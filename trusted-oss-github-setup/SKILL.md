---
name: trusted-oss-github-setup
description: Configure GitHub repositories and local workspaces to opt into a self-hosted Trusted OSS Harbor/Gatekeeper registry (mTLS + TRUSTED_OSS_CACHE_URL) while keeping public upstream registries as the zero-config default. Use when onboarding a repository to the Trusted OSS cache, setting OSS_MTLS_CLIENT_CERT/OSS_MTLS_CLIENT_KEY/TRUSTED_OSS_CACHE_URL, or reverting a repo to public upstream registries.
---

# Trusted OSS GitHub & Local Repo Setup

Configure any local or GitHub repository to route **Maven**, **Python (`uv`/`pip`)**, and **Docker** dependencies through a self-hosted **Trusted OSS Harbor / Gatekeeper** cache over mTLS, while preserving **public upstream registries** as the default whenever `TRUSTED_OSS_CACHE_URL` is unset.

---

## Decision Tree: Public Default vs. Trusted Cache Mode

| Scenario | `TRUSTED_OSS_CACHE_URL` | `TRUSTED_OSS_MODE` | Behavior |
| :--- | :--- | :--- | :--- |
| Public / external contributors (default) | *(unset / empty)* | — | Uses Maven Central, PyPI, `cgr.dev`; mTLS step exits `0`. |
| Active dev / pull-through scanning | `https://<your-cache-fqdn>` | `virtual` *(default)* | Cache misses are fetched upstream, scanned (ClamAV + OSV/Trivy), dual-signed (GPG + ML-DSA-65), and cached. |
| Strict production CI (pre-warmed only) | `https://<your-cache-fqdn>` | `trusted` | Serves only pre-warmed, signed-clean artifacts; fails closed on cache miss. |

---

## Critical Constraints (Never Violate)

- **NEVER commit `mtls-pki/`, `*.key`, `*.p12`, or `.env`**: Keep `client.key` and `ca.key` out of git; inject `client.crt` and `client.key` only via GitHub Secrets (`OSS_MTLS_CLIENT_CERT`, `OSS_MTLS_CLIENT_KEY`).
- **NEVER proxy the cache FQDN through Cloudflare orange-cloud**: Proxy mode terminates TLS at Cloudflare and strips the mTLS client certificate before it reaches pfSense HAProxy (`verify required`). Always use **DNS only (grey cloud)** or direct DDNS (e.g. DuckDNS).
- **Keep CI workflows conditional on `vars.TRUSTED_OSS_CACHE_URL`**: Forks and public clones must succeed without mTLS secrets.
- **Check pfSense & double-NAT**: pfSense WebConfigurator must not bind `:443`, HAProxy must have `Trusted-OSS-GitHub-Client-CA` + `verify required`, and any upstream ISP router (e.g., Bell Giga Hub) must forward TCP `443` to pfSense's active WAN IP.

---

## Automated Setup Procedure

Use the bundled self-contained script [`scripts/setup_trusted_oss_repo.py`](scripts/setup_trusted_oss_repo.py) and templates in [`templates/`](templates/).

### 1. Preview Changes (Dry-Run)
```bash
python3 scripts/setup_trusted_oss_repo.py \
  --repo /path/to/repo \
  --github-repo owner/repo \
  --url https://jsigroup-oss.duckdns.org \
  --cert /path/to/mtls-pki/client.crt \
  --key  /path/to/mtls-pki/client.key \
  --dry-run
```

### 2. Apply Configuration to Local Repo & GitHub Repo
```bash
python3 scripts/setup_trusted_oss_repo.py \
  --repo /path/to/repo \
  --github-repo owner/repo \
  --url https://jsigroup-oss.duckdns.org \
  --mode virtual \
  --cert /path/to/mtls-pki/client.crt \
  --key  /path/to/mtls-pki/client.key
```
This automatically:
1. Sets GitHub Secrets `OSS_MTLS_CLIENT_CERT` and `OSS_MTLS_CLIENT_KEY` via `gh secret set`.
2. Sets GitHub Variables `TRUSTED_OSS_CACHE_URL` and `TRUSTED_OSS_MODE` via `gh variable set`.
3. Configures local `.mvn/settings.xml` + `.mvn/maven.config` (if `pom.xml`/`build.gradle` exists), `uv.toml` (if `pyproject.toml`/`requirements.txt` exists), and `.env` (`TRUSTED_OSS_CACHE_URL`, `TRUSTED_OSS_MODE`, `PIP_INDEX_URL`, `UV_INDEX_URL`, `BASE_IMAGE`).

### 3. Add the Workflow Step to `.github/workflows/*.yml`
Include the conditional setup snippet from [`templates/github-actions-trusted-oss.yml`](templates/github-actions-trusted-oss.yml) (and [`templates/maven-settings.xml`](templates/maven-settings.xml) for Maven builds) before dependency installation/build steps.

### 4. Verify End-to-End Connectivity
```bash
# Direct mTLS check from an allowlisted runner or LAN
curl -fsSL --cert /path/to/client.crt --key /path/to/client.key \
  "https://<your-cache-fqdn>/healthz"
```

### 5. Revert a Repository to Public Upstream Registries
```bash
python3 scripts/setup_trusted_oss_repo.py \
  --repo /path/to/repo \
  --github-repo owner/repo \
  --public
```
