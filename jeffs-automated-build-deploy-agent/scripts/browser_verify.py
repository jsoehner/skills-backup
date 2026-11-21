#!/usr/bin/env python3
"""Guided Headless Chrome (CDP) browser verification tool.

Zero third-party Python dependencies (pure stdlib + local google-chrome).
Loads target URL(s), executes optional guided steps (wait, click, navigate),
captures HTTP/DOM/title/console errors, and saves a screenshot.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any

MACOS_CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)


def find_chrome() -> str:
    for candidate in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(candidate)
        if path:
            return path
    for app_path in MACOS_CHROME_CANDIDATES:
        if os.path.isfile(app_path) and os.access(app_path, os.X_OK):
            return app_path
    raise FileNotFoundError("No Chrome/Chromium binary found in PATH or standard macOS Applications paths")


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
            except TimeoutError:
                break

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass


def evaluate_events(events: list[dict[str, Any]], url: str) -> tuple[int | None, list[str], list[str]]:
    """Extract document HTTP status, console errors, and uncaught exceptions from CDP events."""
    http_status: int | None = None
    console_errors: list[str] = []
    exceptions: list[str] = []

    for ev in events:
        m = ev.get("method")
        p = ev.get("params", {})
        if m == "Network.responseReceived":
            resp = p.get("response", {})
            if resp.get("url", "").rstrip("/") == url.rstrip("/") or http_status is None:
                if p.get("type") == "Document":
                    http_status = resp.get("status")
        elif m == "Runtime.consoleAPICalled" and p.get("type") == "error":
            args = [str(a.get("value", a.get("description", ""))) for a in p.get("args", [])]
            console_errors.append(" ".join(args))
        elif m == "Runtime.exceptionThrown":
            desc = p.get("exceptionDetails", {}).get("text", "exception")
            exceptions.append(desc)

    return http_status, console_errors, exceptions


def clicks_succeeded(click_result: Any) -> bool:
    """Return True if no requested click selector was missing."""
    if click_result is None:
        return True
    if isinstance(click_result, str):
        return click_result == "CLICKED"
    if isinstance(click_result, list):
        return all(isinstance(item, dict) and item.get("status") == "CLICKED" for item in click_result)
    return False


def compute_verdict(result: dict[str, Any], allow_console_errors: bool = False) -> bool:
    """Determine overall pass/fail boolean from collected browser verification results."""
    status_ok = result["http_status"] is None or (200 <= int(result["http_status"]) < 400)
    text_ok = result["expect_text_found"] is not False
    has_content = bool(result["title"] or result["body_snippet"])
    console_ok = allow_console_errors or not result["console_errors"]
    clicks_ok = clicks_succeeded(result.get("click_result"))
    return bool(status_ok and text_ok and has_content and not result["exceptions"] and console_ok and clicks_ok)


def _slugify(text: str, max_len: int = 32) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (slug[:max_len].strip("-")) or "step"


def capture_screenshot(
    client: SimpleCDPClient,
    out_path: str | Path,
    *,
    step: str = "final",
    full_page: bool = False,
) -> dict[str, Any] | None:
    """Capture a PNG screenshot via CDP and write it to out_path."""
    params: dict[str, Any] = {"format": "png"}
    if full_page:
        params["captureBeyondViewport"] = True
    shot = client.send("Page.captureScreenshot", params)
    b64 = shot.get("result", {}).get("data")
    if not b64:
        return None
    raw = base64.b64decode(b64)
    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_bytes(raw)
    return {"step": step, "path": str(out_p), "bytes": len(raw)}


def verify_url(
    url: str,
    wait_seconds: float = 3.0,
    screenshot_path: str | None = None,
    screenshot_dir: str | None = None,
    full_page: bool = False,
    click_selectors: list[str] | None = None,
    expect_text: str | None = None,
    allow_console_errors: bool = False,
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
        "screenshots": [],
        "expect_text_found": None,
        "click_result": None,
    }
    client: SimpleCDPClient | None = None
    shot_dir = Path(screenshot_dir) if screenshot_dir else None
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

        if shot_dir:
            cap = capture_screenshot(client, shot_dir / "00-initial.png", step="initial", full_page=full_page)
            if cap:
                result["screenshots"].append(cap)

        if click_selectors:
            click_results: list[dict[str, Any]] = []
            for idx, sel in enumerate(click_selectors, 1):
                js_click = f"""(() => {{
                    const el = document.querySelector({json.dumps(sel)});
                    if (!el) return "NOT_FOUND";
                    el.click();
                    return "CLICKED";
                }})()"""
                click_res = client.send("Runtime.evaluate", {"expression": js_click, "returnByValue": True})
                status_val = click_res.get("result", {}).get("result", {}).get("value")
                click_results.append({"selector": sel, "status": status_val})
                client.drain_events(1.0)
                if shot_dir:
                    fname = f"{idx:02d}-click-{_slugify(sel)}.png"
                    cap = capture_screenshot(client, shot_dir / fname, step=f"click:{sel}", full_page=full_page)
                    if cap:
                        result["screenshots"].append(cap)
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

        http_status, console_errors, exceptions = evaluate_events(client.events, url)
        result["http_status"] = http_status
        result["console_errors"] = console_errors
        result["exceptions"] = exceptions

        if screenshot_path:
            cap = capture_screenshot(client, screenshot_path, step="final", full_page=full_page)
            if cap:
                result["screenshots"].append(cap)

        result["ok"] = compute_verdict(result, allow_console_errors=allow_console_errors)
        if not result["ok"] and shot_dir and not screenshot_path:
            try:
                cap = capture_screenshot(client, shot_dir / "error.png", step="error", full_page=full_page)
                if cap:
                    result["screenshots"].append(cap)
            except Exception:
                pass
    except Exception as exc:
        result["error"] = str(exc)
        if client and (shot_dir or screenshot_path):
            err_target = (shot_dir / "error.png") if shot_dir else Path(screenshot_path)  # type: ignore[arg-type]
            try:
                cap = capture_screenshot(client, err_target, step="error", full_page=full_page)
                if cap:
                    result["screenshots"].append(cap)
            except Exception:
                pass
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guided headless Chrome browser verifier (CDP).")
    parser.add_argument("url", help="Target URL to open and verify")
    parser.add_argument("--wait", type=float, default=3.0, help="Seconds to wait after navigation")
    parser.add_argument("--screenshot", default="", help="Optional PNG path to save final screenshot")
    parser.add_argument(
        "--screenshot-dir",
        default="",
        help="Optional directory to save multi-step screenshots (00-initial.png, per-click, error.png)",
    )
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="Capture full scrollable page beyond the initial viewport",
    )
    parser.add_argument("--click", action="append", default=[], help="Optional CSS selector(s) to click sequentially after load")
    parser.add_argument("--expect", default="", help="Optional case-insensitive text expected on page")
    parser.add_argument(
        "--allow-console-errors",
        action="store_true",
        help="Do not fail verification when console.error messages are recorded",
    )
    args = parser.parse_args(argv)

    res = verify_url(
        args.url,
        wait_seconds=args.wait,
        screenshot_path=args.screenshot or None,
        screenshot_dir=args.screenshot_dir or None,
        full_page=args.full_page,
        click_selectors=args.click or None,
        expect_text=args.expect or None,
        allow_console_errors=args.allow_console_errors,
    )
    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
