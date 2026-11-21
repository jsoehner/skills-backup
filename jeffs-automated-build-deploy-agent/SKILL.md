---
name: jeffs-automated-build-deploy-agent
description: Systematically check out the top active GitHub repositories one at a time, enforce fork guardrails, onboard each repo to the local Trusted OSS split-horizon registry, build and run the solution, verify functionality with guided headless Chrome browser testing and curl API probes, and commit verification documentation only for functionally verified projects. Use for recurring automated build, run, and functional verification sweeps across GitHub repositories.
---

# Jeffs' Automated Build and Deploy Agent

Systematically clones or updates your top active GitHub repositories **one at a time**, configures each for the local **Trusted OSS Harbor / Gatekeeper** split-horizon registry, builds and runs the application, verifies functionality using **guided headless Chrome (CDP)** and **`curl` API probes**, and commits verification documentation (`docs/BUILD_VERIFICATION.md` + `README.md` badge/link) **only** for functionally verified projects.

Battle-tested across a full 25-repository sweep (18 verified, 4 genuine CVE 451 blocks, 1 platform gate, 1 TS7 regression, 1 code regression).

---

## Bundled Scripts

| Script | Purpose |
| :--- | :--- |
| [`scripts/discover_top_repos.py`](scripts/discover_top_repos.py) | Ranks non-fork, non-archived GitHub repos by commit activity via GraphQL (avoids `pushedAt` distortion from bulk governance/README commits). |
| [`scripts/browser_verify.py`](scripts/browser_verify.py) | Zero-dependency guided headless Chrome (CDP) verifier: navigates URLs, executes sequential multi-step clicks (`--click` repeatable), asserts full-DOM `--expect` text, captures HTTP status, title, console errors, JS exceptions, and PNG screenshots (`--screenshot`). |
| [`scripts/api_verify.py`](scripts/api_verify.py) | `curl`-based API functional verifier supporting `HEAD` (`-I`), binary responses (`<binary: N bytes>`), JSON validation, and expected HTTP status assertions (`--expect-status` or inline `URL=403`). |

---

## Mandatory Sequential Protocol (Per Repository)

Execute repositories **one at a time** to prevent port collisions, Docker resource contention, and Harbor scan races.

### Step 0: Pre-Flight & Target Discovery
1. Run memory pre-flight: `python3 ~/memory_system/inspect_memory.py --preflight .`
2. Discover the top N active repositories:
   ```bash
   python3 ~/.gemini/config/skills/jeffs-automated-build-deploy-agent/scripts/discover_top_repos.py --owner jsoehner --top 25
   ```
3. Check local Trusted OSS LAN cache health:
   ```bash
   curl -sS -o /dev/null -w "%{http_code}\n" http://oss.jsigroup.local:8080/healthz
   ```

### Step 1: Checkout / Update & Fork Guardrail
1. Check if `/home/jsoehner/<repo>` exists and `git remote get-url origin` matches `jsoehner/<repo>`.
   - Preserve any pre-existing uncommitted local edits (check `git diff --name-only <branch>..origin/<branch>` before pulling).
   - Pull safely with explicit remote/branch: `git fetch && git pull --ff-only origin <branch>`.
   - Otherwise clone via `gh repo clone jsoehner/<repo> /home/jsoehner/<repo>` (use `-- --depth 1` for large binary/mobile repos).
2. Run the mandatory fork guardrail check:
   ```bash
   python3 ~/memory_system/check_fork_guardrail.py /home/jsoehner/<repo>
   ```
   If `BLOCKED`, **HALT** immediately — never modify or push to an active fork.

### Step 2: Trusted OSS Split-Horizon Setup & Git Hygiene
1. Run `trusted-oss-github-setup`:
   ```bash
   python3 ~/.gemini/config/skills/trusted-oss-github-setup/scripts/setup_trusted_oss_repo.py \
     --repo /home/jsoehner/<repo> \
     --github-repo jsoehner/<repo> \
     --local-url http://oss.jsigroup.local:8080 \
     --github-url https://jsigroup-oss.duckdns.org \
     --mode virtual \
     --cert /home/jsoehner/trusted-oss-harbor/mtls-pki/client.crt \
     --key  /home/jsoehner/trusted-oss-harbor/mtls-pki/client.key
   ```
2. **Enforce `.git/info/exclude` Hygiene (CRITICAL)**:
   Ensure `.env`, `uv.toml`, `.mvn/settings.xml`, `.mvn/maven.config`, and `.npmrc` are in `.git/info/exclude` (in addition to `.gitignore`) so LAN-only `.local` URLs and `.env` files are **never** committed or pushed to GitHub.
   Also check any pre-existing gitignored `docker-compose.override.yml` for stale `/pypi/trusted/simple` URLs when running `--mode virtual`.

### Step 3: Manifest-First Stack Detection & Battle-Tested Workarounds
**Never trust GitHub's `primaryLanguage`** (helper scripts skew it). Inspect repo manifests and apply these rules:

- **Early Platform Pre-Check (iOS / macOS / Android)**:
  - On Linux hosts, if `.xcodeproj`/`.xcworkspace`/`Podfile` is present with no Linux backend, immediately classify as `BLOCKED (Platform: macOS/Xcode required)`.
  - For dual-platform repos (e.g., Android + PWA/Wasm), verify the Linux-runnable PWA/Wasm components end-to-end and transparently note the Android SDK/NDK/JDK boundary.
- **Maven 3.9+ (`pom.xml`)**:
  - Rewrite `.mvn/maven.config` with `-s` and `.mvn/settings.xml` on **separate lines** (preserving pre-existing flags like `-Daether.remoteRepositoryFilter.prefixes=false`).
  - Pass `-Dmaven.artifact.threads=1` to avoid transient HTTP `451` races on large JARs (`>10 MB`).
  - For multi-module builds where module 1 fails on a CVE gate, run `-pl <remaining> -fae` to surface sibling CVE blocks in one pass.
  - **Distinguish Real CVE 451 vs Transient Scan 451**: Probe the URL with `curl -sS -i -r 0-512 <artifact-url>`. If Harbor returns JSON `Vulnerability gate rejected artifact: High/Critical defect CVSS ...`, treat it as a **genuine security block** — never bypass it; report the artifact, GHSAs, and patched version.
- **Gradle 7+/9+ (`build.gradle`, `gradlew`)**:
  - When using a local LAN HTTP Trusted OSS cache (`TRUSTED_OSS_ENDPOINT` starting with `http://`), pass a temporary `--init-script /tmp/gradle-allow-insecure.gradle` that BOTH rewrites `repo.maven.apache.org/maven2` to `${TRUSTED_OSS_ENDPOINT:-http://oss.jsigroup.local:8080}/maven/virtual` AND sets `allowInsecureProtocol = true`. In CI with HTTPS mTLS (`TRUSTED_OSS_ACTIVE=true`), `GRADLE_OPTS` is already configured.
  - Check host JDK versions (`java -version` vs `JavaLanguageVersion.of(...)` in `build.gradle`).
- **Python (`pyproject.toml`, `requirements.txt`)**:
  - Run `PYTHONPYCACHEPREFIX=/tmp/pycache-<repo> PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q ...` early to catch syntax/indentation regressions and avoid root-owned `__pycache__` collisions.
  - Avoid broken user-local `pytest` shims; create an isolated `/tmp/venv-<repo>` or use `uv run --with pytest pytest -o cache_dir=/tmp/pytest-cache-<repo> --durations=10` (passing `--index-url "${PIP_INDEX_URL:-http://oss.jsigroup.local:8080/pypi/virtual/simple}"` when Trusted OSS is active).
  - For sdist-only packages (e.g., `reverse-geocoder==1.5.1`) or CPython 3.15 sdist builds blocked by `uv.toml`'s `no-build = true`, pass `--no-config` (and `--index-url "$PIP_INDEX_URL"` if set).
  - Watch for EOL Python base images (e.g., `python:3.9-slim`) forcing `pip` onto CVE-blocked `urllib3-2.6.3`.
- **Node.js / TypeScript (`package.json`)**:
  - Trusted OSS Harbor currently returns `404` for `/npm/`; install via `npm ci` (or `--registry=https://registry.npmjs.org --no-package-lock` if a tracked `.npmrc` points to `.local`).
  - Run BOTH `npm run build`/`typecheck` AND `npm test` (esbuild/`tsx` can pass tests while `tsc` fails, e.g., TS 7 `TS5108`).
  - Use `npx vitest run --root <testdir>` if root-owned runtime directories (`data/raft`) cause `EACCES`.
- **Rust / WebAssembly (`Cargo.toml`, `wasm-pack`)**:
  - Ensure `PATH="$HOME/.cargo/bin:$PATH"`. Use `CARGO_TARGET_DIR=/tmp/<repo>-target` if `target/` has tracked legacy files. For `cdylib` Wasm crates, run `cargo test --lib` if `src/main.rs` is a scratch file.
- **Docker / SELinux `Enforcing` / Isolated Ports**:
  - Check `docker ps` and listening ports before launching anything; never disturb pre-existing containers or live services.
  - On Fedora/RHEL SELinux `Enforcing` hosts, mount host directories with `:z` (or `:ro,z`), or stage Compose bind-mounts in `/tmp/<repo>-verify` with a temporary override file adding `:z` (clean root-owned files via `docker run --rm -v /tmp/<repo>-verify:/cleanup:z alpine:latest rm -rf ...`).
  - Run verification servers on isolated ports with temporary SQLite/data directories (`PORT=13001 DATABASE_URL=/tmp/<repo>-verify.sqlite`).
- **Live Infrastructure / OPA / K8s / CI-Release Repos**:
  - **Live Infra (`trusted-oss-harbor`, `rootCA`)**: Read-only health checks, syntax checks, and isolated unit tests only; never restart services or mutate live certs/keys.
  - **OPA Policy Bundles**: Run `openpolicyagent/opa:latest` (`check`, `test`, `build`, ephemeral REST server) with `:ro,z`.
  - **Self-Extracting K8s Generators**: Extract into `/tmp/<repo>-verify`, syntax-check generated scripts, validate all embedded YAML docs via `yaml.safe_load_all`, and test local PKI steps with a read-only `kubectl` shim.
  - **CI-Driven Release Repos (`nvd-cache`)**: Verify GitHub Releases API via `api_verify.py`, download release artifacts to `/tmp/`, verify SHA-256 digests and archive integrity (`unzip -t`), and check recent scheduled workflow runs.

### Step 4: Functional Verification (Browser + Curl + Unit Tests)
1. **Target Repo Config**: If `.jsi-verify.yml` (or a configured file) is present in the repo root, prioritize its declared build, start, and functional verification checks.
2. **Unit / Integration Tests**: Execute native test suites.
3. **Guided Browser Verification (Web UIs)** (use `$SKILL_DIR` in CI or `~/.gemini/config/skills/jeffs-automated-build-deploy-agent` locally):
   ```bash
   python3 "${SKILL_DIR:-$HOME/.gemini/config/skills/jeffs-automated-build-deploy-agent}/scripts/browser_verify.py" \
     "https://localhost:3001/" \
     --expect "Expected Text" \
     --click "#btn-step-1" \
     --click "#btn-step-2" \
     --screenshot-dir "/tmp/jsi-verify/screenshots"
   ```
   Use `--screenshot-dir` to automatically capture `00-initial.png`, per-click screenshots (`01-click-*.png`), and `error.png` on failure (add `--full-page` for long scrolling pages).
   Require `ok: true`, HTTP `200`, non-empty title/DOM, `console_errors: []`, `exceptions: []`, and all `--click` selectors found.
4. **`curl` API Verification**:
   ```bash
   python3 "${SKILL_DIR:-$HOME/.gemini/config/skills/jeffs-automated-build-deploy-agent}/scripts/api_verify.py" \
     "https://localhost:3001/health" \
     "https://localhost:3001/protected=403"
   ```
5. **Structured Verdict Output (CI Mode — MANDATORY)**:
   Write `/tmp/jsi-verify/verdict.json` with:
   ```json
   {
     "status": "pass | fail | blocked",
     "summary": "One-sentence summary of verification outcome",
     "checks": [
       {"name": "build", "status": "pass | fail | skip | blocked", "details": "..."}
     ],
     "failure_reason": ""
   }
   ```

### Step 5: Verification-Gated Documentation Update
**ONLY if the repository built and passed functional verification:**
1. Create/update `docs/BUILD_VERIFICATION.md` with date (`YYYY-MM-DD`), attribution to **"Jeffs' Automated build and deploy agent"**, Trusted OSS summary, exact build/run commands, and functional verification evidence.
2. Add a concise verification badge/link in `README.md` pointing to `docs/BUILD_VERIFICATION.md`.
3. Inspect `git status` and `git diff --cached` to confirm **ONLY** documentation files are staged (zero `.env`, zero `uv.toml`, zero `.mvn/settings.xml`, zero test-generated root artifacts, zero keys/secrets).
4. Commit and push:
   ```bash
   git add README.md docs/BUILD_VERIFICATION.md
   git commit -m "docs(verification): record $(date +%F) functional build verification"
   git push -u origin <branch> || (git pull --rebase origin <branch> && git push -u origin <branch>)
   ```

If a repository **fails** to build or cannot be verified, **do NOT push verification docs**; record exact diagnostics and remediation steps in the sweep report.

### Step 6: Cleanup
- Stop all temporary servers and `docker compose down -v` any temporary verification stacks.
- Remove temporary `/tmp/*-verify*`, `/tmp/pycache-*`, `/tmp/pytest-cache-*`, `/tmp/gradle-allow-insecure.gradle`, and any test-generated untracked files in repo root.
- Verify pre-existing containers and user uncommitted edits remain untouched.
