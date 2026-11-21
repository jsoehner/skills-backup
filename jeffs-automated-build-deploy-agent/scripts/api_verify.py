#!/usr/bin/env python3
"""Curl-based API functional verification helper with expected status support."""

from __future__ import annotations

import argparse
import json
import subprocess
from typing import Any


def parse_expected_statuses(spec: str | None) -> set[int] | None:
    if not spec:
        return None
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if part.isdigit():
            code = int(part)
            if 100 <= code <= 599:
                out.add(code)
    return out or None


def split_url_and_expected(url_spec: str, default_expected: set[int] | None) -> tuple[str, set[int] | None]:
    """Split optional inline =STATUS suffix (e.g. https://localhost:3001/me=403).

    Skips inline splitting when the URL contains a query string ('?') so numeric
    query parameters such as '?page=200' are never mistaken for status assertions.
    """
    if "?" not in url_spec and "=" in url_spec:
        candidate_url, status_part = url_spec.rsplit("=", 1)
        parts = [p.strip() for p in status_part.split(",") if p.strip()]
        if (
            candidate_url.startswith(("http://", "https://"))
            and parts
            and all(p.isdigit() and 100 <= int(p) <= 599 for p in parts)
        ):
            return candidate_url, {int(p) for p in parts}
    return url_spec, default_expected


def probe_endpoint(
    url_spec: str,
    method: str = "GET",
    data: str | None = None,
    header: list[str] | None = None,
    timeout: int = 10,
    default_expected: set[int] | None = None,
) -> dict[str, Any]:
    url, expected = split_url_and_expected(url_spec, default_expected)

    cmd = [
        "curl",
        "-sS",
        "-k",
        "-L",
        "--max-time",
        str(timeout),
        *(["-I"] if method.upper() == "HEAD" else ["-X", method]),
        "-w",
        "\n__CURL_META__%{http_code}|%{time_total}|%{content_type}",
    ]
    for h in header or []:
        cmd.extend(["-H", h])
    if data is not None:
        cmd.extend(["-d", data])
    cmd.append(url)

    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        err_text = proc.stderr.decode("utf-8", errors="replace").strip()
        return {
            "url": url,
            "method": method,
            "ok": False,
            "error": err_text or f"curl exit {proc.returncode}",
        }

    raw_body, _, raw_meta = proc.stdout.rpartition(b"\n__CURL_META__")
    meta = raw_meta.decode("utf-8", errors="replace")
    parts = meta.split("|")
    code = int(parts[0]) if parts and parts[0].isdigit() else 0
    try:
        elapsed = float(parts[1]) if len(parts) > 1 else 0.0
    except ValueError:
        elapsed = 0.0
    ctype = parts[2] if len(parts) > 2 else ""

    is_binary = False
    try:
        body = raw_body.decode("utf-8")
    except UnicodeDecodeError:
        is_binary = True
        body = f"<binary: {len(raw_body)} bytes>"

    is_json = False
    if not is_binary:
        try:
            json.loads(body)
            is_json = True
        except Exception:
            pass

    ok = (code in expected) if expected is not None else (200 <= code < 400)
    return {
        "url": url,
        "method": method,
        "status_code": code,
        "expected_statuses": sorted(expected) if expected else "2xx-3xx",
        "elapsed_sec": elapsed,
        "content_type": ctype,
        "is_json": is_json,
        "is_binary": is_binary,
        "body_bytes": len(raw_body),
        "body_preview": body.strip()[:300],
        "ok": ok,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe one or more API endpoints with curl.")
    parser.add_argument(
        "urls",
        nargs="+",
        help="Endpoint URL(s) to probe (optionally append =STATUS when no query string, e.g. https://localhost:3001/me=403)",
    )
    parser.add_argument("-X", "--method", default="GET")
    parser.add_argument("-d", "--data", default=None)
    parser.add_argument("-H", "--header", action="append", default=[])
    parser.add_argument("--expect-status", default="", help="Comma-separated expected HTTP status codes (e.g. 200 or 401,403)")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args(argv)

    default_expected = parse_expected_statuses(args.expect_status)
    results = [
        probe_endpoint(u, args.method, args.data, args.header, args.timeout, default_expected)
        for u in args.urls
    ]
    print(json.dumps(results, indent=2))
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
