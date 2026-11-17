#!/usr/bin/env python3
"""Self-contained setup script for configuring local & GitHub repositories
to use a Trusted OSS Harbor/Gatekeeper cache (or revert to public repos).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


DEFAULT_GPG_EMAIL = "oss-signing@the-techy.com"
PUBLIC_BASE_IMAGE = "cgr.dev/chainguard/wolfi-base:latest"

MAVEN_SETTINGS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 https://maven.apache.org/xsd/settings-1.2.0.xsd">
  <!-- Managed by trusted-oss-github-setup -->
  <mirrors>
    <mirror>
      <id>trusted-oss-harbor</id>
      <name>Trusted OSS Supply Chain Cache</name>
      <url>{maven_url}</url>
      <mirrorOf>*</mirrorOf>
    </mirror>
  </mirrors>
</settings>
"""


def normalize_cache_url(raw_url: str) -> str:
    url = raw_url.strip().rstrip("/")
    if url and "://" not in url:
        url = f"https://{url}"
    return url


def _update_env_file(
    env_path: Path, updates: dict[str, str], remove_keys: set[str] | None = None, dry_run: bool = False
) -> str:
    remove_keys = remove_keys or set()
    existing = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    seen: set[str] = set()
    out: list[str] = []
    for line in existing:
        s = line.strip()
        if not s or s.startswith("#") or "=" not in line:
            out.append(line)
            continue
        k = line.split("=", 1)[0].strip()
        if k in remove_keys:
            continue
        if k in updates:
            out.append(f"{k}={updates[k]}")
            seen.add(k)
        else:
            out.append(line)
    for k, v in updates.items():
        if k not in seen:
            out.append(f"{k}={v}")
    if not dry_run:
        env_path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return "updated" if env_path.exists() else "created"


def configure_local_repo(repo_dir: Path, cache_url: str, mode: str, dry_run: bool) -> list[str]:
    repo_dir = repo_dir.resolve()
    actions: list[str] = []
    norm_url = normalize_cache_url(cache_url)

    has_maven = (repo_dir / "pom.xml").exists() or (repo_dir / "build.gradle").exists() or (repo_dir / ".mvn").exists()
    has_python = (repo_dir / "pyproject.toml").exists() or (repo_dir / "requirements.txt").exists() or (repo_dir / "uv.toml").exists()
    has_docker = (repo_dir / "Dockerfile").exists() or (repo_dir / "docker-compose.yml").exists()

    if not norm_url:
        for p in [repo_dir / ".mvn" / "settings.xml", repo_dir / ".mvn" / "maven.config", repo_dir / "uv.toml"]:
            if p.exists():
                if not dry_run:
                    p.unlink()
                actions.append(f"removed {p.relative_to(repo_dir)} (public default)")
        env_path = repo_dir / ".env"
        if env_path.exists():
            _update_env_file(
                env_path,
                updates={"BASE_IMAGE": PUBLIC_BASE_IMAGE},
                remove_keys={"TRUSTED_OSS_CACHE_URL", "TRUSTED_OSS_MODE", "PIP_INDEX_URL", "UV_INDEX_URL"},
                dry_run=dry_run,
            )
            actions.append("cleared cache overrides in .env")
        return actions or ["no local changes needed (public default)"]

    maven_url = f"{norm_url}/maven/{mode}"
    pypi_url = f"{norm_url}/pypi/{mode}/simple"
    host = urlparse(norm_url).netloc or norm_url

    if has_maven:
        if not dry_run:
            (repo_dir / ".mvn").mkdir(parents=True, exist_ok=True)
            (repo_dir / ".mvn" / "settings.xml").write_text(MAVEN_SETTINGS_TEMPLATE.format(maven_url=maven_url), encoding="utf-8")
            (repo_dir / ".mvn" / "maven.config").write_text("-s .mvn/settings.xml\n", encoding="utf-8")
        actions.append(f"configured .mvn/settings.xml & .mvn/maven.config -> {maven_url}")

    if has_python:
        if not dry_run:
            (repo_dir / "uv.toml").write_text(
                f'# Managed by trusted-oss-github-setup\nindex-url = "{pypi_url}"\nno-build = true\n',
                encoding="utf-8",
            )
        actions.append(f"configured uv.toml -> {pypi_url}")

    env_updates = {"TRUSTED_OSS_CACHE_URL": norm_url, "TRUSTED_OSS_MODE": mode}
    if has_python:
        env_updates["PIP_INDEX_URL"] = pypi_url
        env_updates["UV_INDEX_URL"] = pypi_url
    if has_docker:
        env_updates["BASE_IMAGE"] = f"{host}/v2/{mode}/chainguard/wolfi-base:latest"
    _update_env_file(repo_dir / ".env", updates=env_updates, dry_run=dry_run)
    actions.append(f"updated .env with TRUSTED_OSS_CACHE_URL={norm_url}")
    return actions


def configure_github_repo(
    github_repo: str,
    cache_url: str,
    mode: str,
    gpg_email: str,
    cert_path: Path | None,
    key_path: Path | None,
    dry_run: bool,
) -> list[str]:
    actions: list[str] = []
    norm_url = normalize_cache_url(cache_url)

    if not norm_url:
        if not dry_run:
            subprocess.run(["gh", "variable", "delete", "TRUSTED_OSS_CACHE_URL", "-R", github_repo], check=False, capture_output=True)
        actions.append(f"deleted GitHub variable TRUSTED_OSS_CACHE_URL on {github_repo}")
        return actions

    for name, val in [("TRUSTED_OSS_CACHE_URL", norm_url), ("TRUSTED_OSS_MODE", mode), ("TRUSTED_OSS_GPG_EMAIL", gpg_email)]:
        if not dry_run:
            subprocess.run(["gh", "variable", "set", name, "--body", val, "-R", github_repo], check=True, capture_output=True)
        actions.append(f"set GitHub variable {name}={val} on {github_repo}")

    for sec_name, path in [("OSS_MTLS_CLIENT_CERT", cert_path), ("OSS_MTLS_CLIENT_KEY", key_path)]:
        if path:
            if not path.exists():
                raise FileNotFoundError(f"Missing mTLS credential file: {path}")
            if not dry_run:
                subprocess.run(
                    ["gh", "secret", "set", sec_name, "-R", github_repo, "--body", path.read_text(encoding="utf-8")],
                    check=True,
                    capture_output=True,
                )
            actions.append(f"set GitHub secret {sec_name} from {path} on {github_repo}")
    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure local & GitHub repo for Trusted OSS Harbor or public default.")
    parser.add_argument("--repo", default=".", help="Local repository path (default: .)")
    parser.add_argument("--github-repo", default="", help="GitHub repo (owner/name) for gh secret/variable setup")
    parser.add_argument("--url", default=os.getenv("TRUSTED_OSS_CACHE_URL", ""), help="Default cache URL if --local-url / --github-url are omitted")
    parser.add_argument("--local-url", default=os.getenv("TRUSTED_OSS_LOCAL_URL", ""), help="LAN cache URL for local workspace (e.g. http://oss.jsigroup.local:8080)")
    parser.add_argument("--github-url", default="", help="External WAN mTLS URL for GitHub Actions (e.g. https://jsigroup-oss.duckdns.org)")
    parser.add_argument("--mode", choices=["virtual", "trusted"], default=os.getenv("TRUSTED_OSS_MODE", "virtual"))
    parser.add_argument("--gpg-email", default=os.getenv("TRUSTED_OSS_GPG_EMAIL", DEFAULT_GPG_EMAIL), help="Expected GPG signing key email (default: oss-signing@the-techy.com)")
    parser.add_argument("--cert", default="", help="Path to mTLS client.crt for OSS_MTLS_CLIENT_CERT")
    parser.add_argument("--key", default="", help="Path to mTLS client.key for OSS_MTLS_CLIENT_KEY")
    parser.add_argument("--public", action="store_true", help="Revert to public upstream repos")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files or GitHub")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    local_url = "" if args.public else (args.local_url or args.url)
    github_url = "" if args.public else (args.github_url or args.url)
    local_actions = configure_local_repo(Path(args.repo), local_url, args.mode, args.dry_run)
    gh_actions: list[str] = []
    if args.github_repo:
        gh_actions = configure_github_repo(
            args.github_repo,
            github_url,
            args.mode,
            args.gpg_email,
            Path(args.cert) if args.cert else None,
            Path(args.key) if args.key else None,
            args.dry_run,
        )

    result: dict[str, Any] = {"local": local_actions, "github": gh_actions, "dry_run": args.dry_run}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        prefix = "[DRY-RUN] " if args.dry_run else ""
        for a in local_actions + gh_actions:
            print(f"{prefix}{a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
