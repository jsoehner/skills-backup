---
name: repo-governance-automation
group: software_architecture
description: "Automates the application of a 'Gold Standard' governance suite to any GitHub repository, systematically injecting documentation, DX, workflows, multi-layer security configurations, and dual-engine SBOM/CBOM scanning with automated CI test verification."
version: 2
created: "2026-07-31"
updated: "2026-09-27"
---

# Repository Governance Automation Skill

This skill automates the application of a "Gold Standard" governance suite to any GitHub repository. It works in conjunction with [repo-governance-orchestrator](../repo-governance-orchestrator/SKILL.md) to systematically inject developer experience, security, and dual-engine software/cryptographic supply chain governance (SBOM & CBOM) workflows.

## Applied Governance Suite

The following files are created/updated in each target repository:

### 1. Documentation & DX
- **`CONTRIBUTING.md`**: Standardized guidelines for contributors, including setup instructions, branching strategies, and commit standards.
- **`PULL_REQUEST_TEMPLATE.md`**: A structured template for all PRs to ensure clear descriptions, testing evidence, and checklists.

### 2. Workflow & Automation
- **`commit-lint.yml`**: A GitHub Action that enforces **Conventional Commits** (e.g., `feat:`, `fix:`) on all pushes and PRs.
- **`changelog.yml`**: A GitHub Action that automatically generates a `CHANGELOG.md` based on the Conventional Commit history.

### 3. Dual-Engine Supply Chain & Cryptographic Governance (BOM Suite)
- **`sbom.yml`**: A GitHub Action that generates:
  - Software Bill of Materials (SBOM) in both **CycloneDX** and **SPDX** standard JSON formats via Anchore / Syft.
  - Cryptographic Bill of Materials (CBOM) in CycloneDX format via `@cyclonedx/cdxgen --include-crypto`.
  - Runs dual-engine AST reconciliation (`scripts/scan_crypto_ast.py`) to discover runtime cryptographic call sites across Python, JS/TS, Go, Java, Rust, C#, and C/C++.
  - Runs the automated verification test harness (`scripts/test_boms.sh`).
  - Generates the Post-Quantum Cryptography (PQC) migration scorecard and step summary (`scripts/analyze_cbom.py`).
  - Archives all artifacts to `oss/` and attaches them to GitHub release tags.
- **Bundled Scripts**:
  - `scripts/generate_boms.sh`: Local generator with integrated AST reconciliation.
  - `scripts/scan_crypto_ast.py`: Multi-language semantic AST call-site extractor.
  - `scripts/analyze_cbom.py`: PQC migration analyzer and Markdown generator.
  - `scripts/test_boms.sh`: Verification test harness.

### 4. Security & Hardening
- **`security-testing.yml`**: A multi-layered security pipeline that runs:
  - **Gitleaks**: To detect hardcoded secrets.
  - **Trivy**: To scan container images for vulnerabilities.
  - **Semgrep**: To perform Static Application Security Testing (SAST) on source code.
- **`github-actions-node24` & Security Pinning**: All injected GitHub workflows enforce Node 24 runtime support and 40-character immutable commit SHA pinning on all workflow `uses:` directives.

## Usage

Use the bundled scaffolding script:

```bash
# Full Governance Suite
python3 skills/repo-governance-automation/scripts/scaffold_governance.py /path/to/target-repo

# BOM Scanning Workflow Only
python3 skills/repo-governance-automation/scripts/scaffold_governance.py /path/to/target-repo --mode bom-only
```
