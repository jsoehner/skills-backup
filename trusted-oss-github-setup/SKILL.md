---
name: trusted-oss-github-setup
description: Configure GitHub repositories and local workspaces to opt into a self-hosted Trusted OSS Harbor/Gatekeeper registry (split-horizon LAN vs. WAN mTLS + TRUSTED_OSS_CACHE_URL) while keeping public upstream registries as the zero-config default. Use when onboarding a repository to the Trusted OSS cache, avoiding NAT hairpinning between local LAN and GitHub Actions, setting OSS_MTLS_CLIENT_CERT/OSS_MTLS_CLIENT_KEY/TRUSTED_OSS_CACHE_URL, or reverting a repo to public upstream registries.
---

# Trusted OSS GitHub & Local Repo Setup (Split-Horizon Strategy)

Configure any local or GitHub repository to route **Maven**, **Python (`uv`/`pip`)**, and **Docker** dependencies through a self-hosted **Trusted OSS Harbor / Gatekeeper** cache while solving **NAT hairpinning** and preserving **public upstream registries** as the zero-config default.

---

## Split-Horizon URL Strategy (Solving NAT Hairpinning)

Inside the LAN (behind an ISP router such as Bell Giga Hub + pfSense), connecting to the external FQDN loops back through WAN NAT (**NAT hairpinning**) and often times out or fails mTLS. Always split the endpoint by execution context:

| Context | Variable / Target | Example URL | Transport |
| :--- | :--- | :--- | :--- |
| **Local Development (LAN)** | `--local-url` (`.mvn/`, `uv.toml`, `.env`) | `http://oss.jsigroup.local:8080` | Direct LAN HTTP to TrueNAS `:8080` (no hairpin, no mTLS needed) |
| **GitHub Actions (WAN)** | `--github-url` (`vars.TRUSTED_OSS_CACHE_URL`) | `https://jsigroup-oss.duckdns.org` | Public DNS + pfSense `github_actions_cidrs` + mTLS (`OSS_MTLS_CLIENT_CERT` / `KEY`) |
| **Public Default (Unset)** | *(unset / `--public`)* | Maven Central / PyPI / `cgr.dev` | Direct public upstream registries |

---

## Critical Constraints (Never Violate)

- **NEVER use the external WAN URL for local LAN builds** when behind double-NAT/Bell Giga Hub — use `--local-url http://oss.jsigroup.local:8080`.
- **NEVER commit `mtls-pki/`, `*.key`, `*.p12`, or `.env`**: Keep `client.key` and `ca.key` out of git; inject `client.crt` and `client.key` only via GitHub Secrets (`OSS_MTLS_CLIENT_CERT`, `OSS_MTLS_CLIENT_KEY`).
- **NEVER commit LAN-only `.mvn/settings.xml` or `uv.toml` into public repos** if external contributors/CI shouldn't inherit your private `.local` URL (add them to `.gitignore` or `.git/info/exclude`, or use `--github-url` only for CI).
- **NEVER proxy the external cache FQDN through Cloudflare orange-cloud**: Proxy mode strips the mTLS client certificate before it reaches pfSense HAProxy (`verify required`).
- **Keep CI workflows conditional on `vars.TRUSTED_OSS_CACHE_URL`**: Forks and public clones must succeed without mTLS secrets.

---

## Automated Setup Procedure

Use the bundled self-contained script [`scripts/setup_trusted_oss_repo.py`](scripts/setup_trusted_oss_repo.py) and templates in [`templates/`](templates/).

### 1. Preview Split-Horizon Changes (Dry-Run)
```bash
python3 scripts/setup_trusted_oss_repo.py \
  --repo /path/to/repo \
  --github-repo owner/repo \
  --local-url http://oss.jsigroup.local:8080 \
  --github-url https://jsigroup-oss.duckdns.org \
  --cert /path/to/mtls-pki/client.crt \
  --key  /path/to/mtls-pki/client.key \
  --dry-run
```

### 2. Apply Split-Horizon Configuration
```bash
python3 scripts/setup_trusted_oss_repo.py \
  --repo /path/to/repo \
  --github-repo owner/repo \
  --local-url http://oss.jsigroup.local:8080 \
  --github-url https://jsigroup-oss.duckdns.org \
  --mode virtual \
  --cert /path/to/mtls-pki/client.crt \
  --key  /path/to/mtls-pki/client.key
```
This automatically:
1. Sets GitHub Secrets `OSS_MTLS_CLIENT_CERT` and `OSS_MTLS_CLIENT_KEY` via `gh secret set`.
2. Sets GitHub Variables `TRUSTED_OSS_CACHE_URL=https://jsigroup-oss.duckdns.org` and `TRUSTED_OSS_MODE=virtual` via `gh variable set`.
3. Configures local `.mvn/settings.xml` + `.mvn/maven.config`, `uv.toml`, and `.env` to use `http://oss.jsigroup.local:8080` (no NAT hairpinning).

*(Note: `--url <URL>` can still be used as a shorthand when `--local-url` and `--github-url` are the same.)*

### 3. Add the Workflow Step to `.github/workflows/*.yml`
Include the conditional setup snippet from [`templates/github-actions-trusted-oss.yml`](templates/github-actions-trusted-oss.yml) (and [`templates/maven-settings.xml`](templates/maven-settings.xml) for Maven builds) before dependency installation/build steps.

### 4. Revert a Repository to Public Upstream Registries
```bash
python3 scripts/setup_trusted_oss_repo.py \
  --repo /path/to/repo \
  --github-repo owner/repo \
  --public
```
