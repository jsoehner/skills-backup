# Build & Functional Verification Report

- **Verification Date:** `2026-11-20`
- **Verified By:** **Jeffs' Automated build and deploy agent**
- **Repository:** `jsoehner/skills-backup`
- **Fork Guardrail Status:** `ALLOWED_STANDALONE` (standalone repository, not a fork)
- **Overall Status:** `VERIFIED`

---

## 1. Trusted OSS Split-Horizon Configuration

Configured via `setup_trusted_oss_repo.py` in `virtual` mode:

| Scope | Setting | Value |
| :--- | :--- | :--- |
| Local LAN | `TRUSTED_OSS_CACHE_URL` (`.env`, gitignored) | `http://oss.jsigroup.local:8080` (`healthz` HTTP `200`) |
| GitHub Actions (WAN) | `TRUSTED_OSS_CACHE_URL` (repo variable) | `https://jsigroup-oss.duckdns.org` |
| GitHub Actions | `TRUSTED_OSS_MODE` (repo variable) | `virtual` |
| GitHub Actions | `TRUSTED_OSS_GPG_EMAIL` (repo variable) | `oss-signing@the-techy.com` |
| GitHub Actions | mTLS Secrets | `OSS_MTLS_CLIENT_CERT`, `OSS_MTLS_CLIENT_KEY` |

Git hygiene verified: `.env`, `uv.toml`, `.mvn/settings.xml`, `.mvn/maven.config`, and `.npmrc` are excluded in `.git/info/exclude` so LAN-only URLs and local environment files are never committed.

---

## 2. Detected Stack & Build / Syntax Checks

This repository is a Python, Bash, and PowerShell CLI and agent-skills collection (`494` flattened root-level skills with `SKILL.md`; no web server or HTTP API).

| Check | Command | Result |
| :--- | :--- | :--- |
| Python bytecode compilation | `python3 -m py_compile import_builtins.py scripts/*.py` | PASS |
| Bash syntax check | `bash -n setup.sh scripts/*.sh` | PASS |
| JSON schema/syntax validation | `json.load` on `audit_status.json` and `scripts/known_cbom_catalog.json` | PASS |
| Flattened skill layout check | Verified root-level `*/SKILL.md` count and absence of nested `skills/` | PASS (`494` skills) |

---

## 3. Functional Verification Results

All CLI commands were executed in read-only or isolated temporary-directory mode so live installed client skills (`~/.gemini/config/skills`) remained untouched.

| Verification Test | Command | Result & Observed Output |
| :--- | :--- | :--- |
| CLI Help | `./setup.sh --help` | PASS (exit `0`) |
| Category Listing | `./setup.sh --categories` | PASS (`15` categories, `724` category mappings) |
| Catalog Search | `./setup.sh --catalog -q postgres` | PASS (`18` matching PostgreSQL skills returned) |
| Client Status Diff | `./setup.sh --status --client gemini` | PASS (exit `0`; compared repo vs installed skills) |
| Fork Guardrail CLI | `./setup.sh --check-fork .` | PASS (`ALLOWED_STANDALONE`) |
| Repository & Memory Info | `./setup.sh --info` | PASS (`33` OKF policies, `44` ChromaDB records) |
| Memory JSON Export | `python3 scripts/inspect_memory.py --json` | PASS (valid JSON: `chroma_collection`, `inbox_stats`, `okf_collection`, `root_dir`, `status`) |
| Isolated Skill Restore | `HOME="$TMP_HOME" python3 scripts/restore_skills.py . --client gemini` | PASS (`494` unique skills + governance rules restored to isolated temp `$HOME`, then cleaned up) |
| SBOM & CBOM Test Harness | `bash scripts/test_boms.sh oss` | PASS (`4/4` checks passed: SPDX SBOM + CycloneDX v1.7 CBOM valid, `5` crypto assets audited at `100.0%` confidence) |
| Web UI / HTTP API | N/A | Repository has no web UI or HTTP server |
