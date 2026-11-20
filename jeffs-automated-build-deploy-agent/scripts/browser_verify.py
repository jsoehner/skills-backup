#!/usr/bin/env python3
"""Guided Headless Chrome (CDP) browser verification tool.

Zero third-party Python dependencies (pure stdlib + local google-chrome).
Loads target URL(s), executes optional guided steps (wait, click, navigate),
captures HTTP/DOM/title/console errors, and saves a screenshot.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any


def find_chrome() -> str:
    for candidate in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError("No Chrome/Chromium binary found in PATH")


def pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class SimpleCDPClient:
    """Minimal RFC 6455 WebSocket client for Chrome DevTools Protocol."""

    def __init__(self, ws_url: str, timeout: float = 20.0) -> None:
        assert ws_url.startswith("ws://"), f"Unsupported ws_url: {ws_url}"
        rest = ws_url[5:]
        host_port, path = rest.split("/", 1)
        path = "/" + path
        host, port_s = host_port.split(":")
        self.sock = socket.create_connection((host, int(port_s)), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode("ascii"))
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("WebSocket handshake closed prematurely")
            buf += chunk
        header_part, self._extra = buf.split(b"\r\n\r\n", 1)
        if b"101 " not in header_part.splitlines()[0]:
            raise ConnectionError(f"WebSocket handshake failed: {header_part!r}")
        self._msg_id = 0
        self.events: list[dict[str, Any]] = []

    def _recv_exact(self, n: int) -> bytes:
        out = bytearray()
        if self._extra:
            take = min(n, len(self._extra))
            out.extend(self._extra[:take])
            self._extra = self._extra[take:]
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise ConnectionError("WebSocket closed during read")
            out.extend(chunk)
        return bytes(out)

    def _send_frame(self, payload: bytes, opcode: int = 1) -> None:
        mask = os.urandom(4)
        header = bytearray([0x80 | opcode])
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + masked)

    def _recv_frame(self) -> tuple[int, bytes]:
        b1, b2 = self._recv_exact(2)
        opcode = b1 & 0x0F
        masked = (b2 & 0x80) != 0
        length = b2 & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._recv_exact(8))[0]
        mask = self._recv_exact(4) if masked else b""
        data = self._recv_exact(length)
        if masked:
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        return opcode, data

    def send(self, method: str, params: dict[str, Any] | None = None, timeout: float = 15.0) -> dict[str, Any]:
        self._msg_id += 1
        req_id = self._msg_id
        msg = {"id": req_id, "method": method, "params": params or {}}
        self._send_frame(json.dumps(msg).encode("utf-8"))
        self.sock.settimeout(timeout)
        deadline = time.time() + timeout
        while time.time() < deadline:
            opcode, data = self._recv_frame()
            if opcode == 9:  # ping -> pong
                self._send_frame(data, opcode=10)
                continue
            if opcode == 8:  # close
                raise ConnectionError("WebSocket closed by browser")
            if opcode != 1:
                continue
            obj = json.loads(data.decode("utf-8"))
            if obj.get("id") == req_id:
                return obj
            self.events.append(obj)
        raise TimeoutError(f"CDP call timed out: {method}")

    def drain_events(self, duration: float = 1.0) -> None:
        end = time.time() + duration
        while time.time() < end:
            remaining = max(0.05, end - time.time())
            self.sock.settimeout(remaining)
            try:
                opcode, data = self._recv_frame()
                if opcode == 1:
                    self.events.append(json.loads(data.decode("utf-8")))
            except (socket.timeout, TimeoutError):
                break

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass


def verify_url(
    url: str,
    wait_seconds: float = 3.0,
    screenshot_path: str | None = None,
    click_selectors: list[str] | None = None,
    expect_text: str | None = None,
) -> dict[str, Any]:
    chrome = find_chrome()
    port = pick_free_port()
    user_data_dir = tempfile.mkdtemp(prefix="chrome-verify-")
    proc = subprocess.Popen(
        [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--ignore-certificate-errors",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}",
            "--window-size=1280,900",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    result: dict[str, Any] = {
        "url": url,
        "ok": False,
        "title": "",
        "final_url": "",
        "body_snippet": "",
        "console_errors": [],
        "exceptions": [],
        "http_status": None,
        "screenshot": screenshot_path,
        "expect_text_found": None,
        "click_result": None,
    }
    client: SimpleCDPClient | None = None
    try:
        ws_url = None
        for _ in range(40):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1.0) as resp:
                    targets = json.loads(resp.read().decode("utf-8"))
                for t in targets:
                    if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                        ws_url = t["webSocketDebuggerUrl"]
                        break
                if ws_url:
                    break
            except Exception:
                time.sleep(0.25)
        if not ws_url:
            raise RuntimeError("Timed out waiting for Chrome DevTools target")

        client = SimpleCDPClient(ws_url)
        client.send("Page.enable")
        client.send("Runtime.enable")
        client.send("Network.enable")
        client.send("Log.enable")
        client.send("Page.navigate", {"url": url})
        client.drain_events(wait_seconds)

        if click_selectors:
            click_results: list[dict[str, Any]] = []
            for sel in click_selectors:
                js_click = f"""(() => {{
                    const el = document.querySelector({json.dumps(sel)});
                    if (!el) return "NOT_FOUND";
                    el.click();
                    return "CLICKED";
                }})()"""
                click_res = client.send("Runtime.evaluate", {"expression": js_click, "returnByValue": True})
                click_results.append({"selector": sel, "status": click_res.get("result", {}).get("result", {}).get("value")})
                client.drain_events(1.0)
            result["click_result"] = click_results[0]["status"] if len(click_results) == 1 else click_results

        expect_expr = json.dumps(expect_text.lower()) if expect_text else "null"
        eval_res = client.send(
            "Runtime.evaluate",
            {
                "expression": (
                    "(() => { "
                    "const t = document.title || ''; "
                    "const full = document.body ? document.body.innerText : ''; "
                    f"const exp = {expect_expr}; "
                    "return JSON.stringify({"
                    "title: t, href: location.href, text: full.slice(0, 600), "
                    "expectFound: exp === null ? null : (t + ' ' + full).toLowerCase().includes(exp)"
                    "}); })()"
                ),
                "returnByValue": True,
            },
        )
        raw_val = eval_res.get("result", {}).get("result", {}).get("value", "{}")
        info = json.loads(raw_val) if isinstance(raw_val, str) else {}
        result["title"] = info.get("title", "")
        result["final_url"] = info.get("href", "")
        result["body_snippet"] = " ".join(info.get("text", "").split())[:400]
        if expect_text:
            result["expect_text_found"] = info.get("expectFound")

        for ev in client.events:
            m = ev.get("method")
            p = ev.get("params", {})
            if m == "Network.responseReceived":
                resp = p.get("response", {})
                if resp.get("url", "").rstrip("/") == url.rstrip("/") or result["http_status"] is None:
                    if p.get("type") == "Document":
                        result["http_status"] = resp.get("status")
            elif m == "Runtime.consoleAPICalled" and p.get("type") == "error":
                args = [str(a.get("value", a.get("description", ""))) for a in p.get("args", [])]
                result["console_errors"].append(" ".join(args))
            elif m == "Runtime.exceptionThrown":
                desc = p.get("exceptionDetails", {}).get("text", "exception")
                result["exceptions"].append(desc)

        if screenshot_path:
            shot = client.send("Page.captureScreenshot", {"format": "png"})
            b64 = shot.get("result", {}).get("data")
            if b64:
                out_p = Path(screenshot_path)
                out_p.parent.mkdir(parents=True, exist_ok=True)
                out_p.write_bytes(base64.b64decode(b64))

        status_ok = result["http_status"] is None or (200 <= int(result["http_status"]) < 400)
        text_ok = result["expect_text_found"] is not False
        has_content = bool(result["title"] or result["body_snippet"])
        result["ok"] = bool(status_ok and text_ok and has_content and not result["exceptions"])
    except Exception as exc:
        result["error"] = str(exc)
    finally:
        if client:
            client.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        shutil.rmtree(user_data_dir, ignore_errors=True)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Guided headless Chrome browser verifier (CDP).")
    parser.add_argument("url", help="Target URL to open and verify")
    parser.add_argument("--wait", type=float, default=3.0, help="Seconds to wait after navigation")
    parser.add_argument("--screenshot", default="", help="Optional PNG path to save screenshot")
    parser.add_argument("--click", action="append", default=[], help="Optional CSS selector(s) to click sequentially after load")
    parser.add_argument("--expect", default="", help="Optional case-insensitive text expected on page")
    args = parser.parse_args()

    res = verify_url(
        args.url,
        wait_seconds=args.wait,
        screenshot_path=args.screenshot or None,
        click_selectors=args.click or None,
        expect_text=args.expect or None,
    )
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
