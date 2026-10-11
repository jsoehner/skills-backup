# Changelog

## [Unreleased]
### Added
- **Timestamped Skill Restoration & Status Inspection**: Added date stamp prefixes (`[YYYY-MM-DD HH:MM:SS]`) at the beginning of each restored skill line in `scripts/restore_skills.py`, added runtime date stamps to the startup banner in `setup.sh` and `setup.ps1`, and added timestamp prefixes for existing/installed and new skills in `scripts/catalog.py` (`--status` and `--installed`).
- **OCI Distribution Spec v1.1+ & ORAS Graph Support for CBOMs**: Upgraded `sbom-cbom-generator` to align with the modern OCI artifact standard where vendors attach CBOM/SBOM artifacts alongside images via the `subject` field rather than embedding them into image layers. Added `scripts/fetch_oci_cbom.py` to discover and fetch attached vendor CBOMs (`application/vnd.cyclonedx+json`) via the OCI Referrers API / ORAS without pulling whole containers. Added `scripts/attach_oci_bom.sh` to publish generated CBOMs/SBOMs as attached OCI 1.1 graph artifacts.
- **Zero-Analysis Upstream & Open-Source CBOM Assimilation**: Enhanced `scripts/generate_boms.sh` and `scripts/analyze_cbom.py` with `--external-cbom` flags and expanded `scripts/known_cbom_catalog.json` with open-source infrastructure and system library profiles (OpenSSL, `libssl3`, `libcrypto3`, Mozilla `ca-certificates`, NGINX, Envoy, cURL). Enables automated assimilation of third-party and base-image crypto assets into comprehensive PQC audit reports without running heavy, invasive scans on third-party binaries.
- **Node 24 & Hardened CI/CD Workflow Modernization**: Updated `references/workflow_template.yml` and `scripts/install_to_repo.sh` to leverage Node 24 (`actions/checkout@v7`), `oras-project/setup-oras@v1.2.2`, and multi-layer verification testing for automated supply chain attestation.
- **Repository Governance Orchestrator Skill**: Added master sequential orchestrator `repo-governance-orchestrator` under Architecture & Engineering Practices (`software_architecture`) along with GitHub templates for contributing guidelines, pull request template, commit-lint configuration, changelog generation workflow, security testing pipeline (Gitleaks, Trivy, Semgrep), and dual-engine Software & Cryptographic Bill of Materials (SBOM/CBOM) scanning with AST discovery, automated CI verification test harness, and PQC migration scorecards.
- **SBOM & CBOM Generator Skill**: Added `sbom-cbom-generator` under Security, Compliance & Hardening (`security_compliance`) to generate, validate, and manage Software Bill of Materials (SBOM) and Cryptographic Bill of Materials (CBOM) for container images and source code directories using Anchore Syft and CycloneDX `cdxgen`. Features automated Post-Quantum Cryptography (PQC) readiness assessment (`analyze_cbom.py`), multi-layer verification tests (`test_boms.sh`), and one-step target repository scaffolding (`install_to_repo.sh`).
- **Security Governance Orchestrator Expansion**: Upgraded `security-governance-orchestrator` to version 2, incorporating supply chain & cryptographic governance procedures (Phase 4), PQC readiness tracking, and strict anti-pattern rules against releasing software without validated machine-readable BOM artifacts.
### Changed
- **CBOM Scanning Action Migration**: Migrated CBOM scanning in `sbom-cbom-generator` (`install_to_repo.sh`, `workflow_template.yml`, and `SKILL.md`), `repo-governance-orchestrator` (`templates/sbom.yml`), and `.github/workflows/sbom-cbom.yml` from `cdxgen` npm actions to `cbomkit/cbomkit-action` (pinned to commit SHA `34a3d96...` / v2.3.0), eliminating Node.js setup overhead and standardizing on PQCA Sonar Cryptography container-based CBOM generation.
- **Cryptographic Call-Site Location Reporting & In-Repo Publishing**: Enriched `scan_crypto_ast.py` and `analyze_cbom.py` to aggregate all file occurrences, line numbers, and code snippets into CBOM components. Added explicit `Location(s)` columns and a dedicated "Developer & Security Remediation Guide" to markdown summaries (`docs/security/CRYPTOGRAPHIC_AUDIT.md`). Updated workflow templates and installers to automatically commit and publish the audit report back to the repository on push (using `[skip ci]`) for transparent tracking across security and engineering teams.
### Fixed
- **CBOM Location Formatting & Harness Runtime Stability**: Fixed `NameError: name 'format_locations' is not defined` in `sbom-cbom-generator/scripts/analyze_cbom.py` when generating markdown assessments and restored the unassimilated dependencies table. Reconfigured stdout and stderr to UTF-8 with fallback replacement to prevent `UnicodeEncodeError` in Windows cp1252 local AI harnesses and CLI runs. Corrected `Path` object string comparison for `--json` output so STDOUT redirection prints valid JSON instead of creating a file. Added unit test coverage for markdown report generation.
- **CBOM Assimilation Variable Reference**: Fixed undefined variable error in `scripts/analyze_cbom.py` during third-party dependency matching.
- **AST Self-Scanning Isolation**: Excluded `scripts/`, `tests/`, and internal tool files from `scan_crypto_ast.py` directory traversal to prevent false-positive self-scanning of the scanner's own algorithm dictionary. Refined deduplication logic to prevent collision between `SHA-3` and `SHA-384`. Configured `CBOMKIT_EXCLUDE` in CI workflows to only analyze production application code.

## [1.3.0] - 2026-09-07
### Changed
- **Deploy Script Root Resolution**: Fixed `scripts/deploy_skills.py` repository root resolution (`REPO_DIR`) so it dynamically references the repository root when executed from within the centralized `scripts/` directory.
- **Directory Traversal Pruning**: Hardened filesystem traversal in `scripts/deploy_skills.py` by pruning hidden folders and `__pycache__` directories in-place during `os.walk`.

### Added
- **New Master Orchestrators**: Added 6 additional orchestrator skills for comprehensive lifecycle management:
  - `data-platform-orchestrator`: End-to-end data engineering (Schema $\rightarrow$ dbt $\rightarrow$ Quality $\rightarrow$ Analysis).
  - `security-audit-orchestrator`: Full security audit lifecycle (Threat Modeling $\rightarrow$ Scanning $\rightarrow$ Forensics $\rightarrow$ Reporting).
  - `mlops-pipeline-orchestrator`: Production ML lifecycle (Training $\rightarrow$ Deployment $\rightarrow$ Monitoring).
  - `frontend-design-system-orchestrator`: UI/UX and design system consistency (Design $\rightarrow$ Tokens $\rightarrow$ Components $\rightarrow$ Validation).
  - `startup-strategy-orchestrator`: Startup planning and financial modeling (Market $\rightarrow$ Finance $\rightarrow$ Operations $\rightarrow$ Synthesis).
  - `multimedia-production-orchestrator`: Multimedia production (Download $\rightarrow$ Brand $\rightarrow$ Edit $\rightarrow$ Render $\rightarrow$ Landing Page).

- **Root Directory CLI Flag**: Added `--root-dir` parameter to `scripts/deploy_skills.py` allowing custom root directory paths for tests, CI/CD, and sub-tree deployments.
- **Architecture Decision Record**: Documented deployment script root path resolution and traversal hardening in [ADR-0013](docs/adr/0013-deploy-skills-root-resolution-and-traversal-hardening.md).
- **Multi-Client Setup Tooling**: Added `setup.sh` (Bash) and `setup.ps1` (PowerShell) for fast cross-client environment setup, status inspection (`--status`), catalog browsing (`--catalog`), and memory diagnostics (`--memory`).
- **Catalog Inspection Engine**: Added `scripts/catalog.py` for diffing installed vs. repository skills and inspecting memory system health.

### Documentation
- **ADR Directory Reconciliation**: Consolidated legacy decision directories into `docs/adr/` with updated governance strategy references.
- **Operational Guides**: Updated `DEVELOPER_GUIDE.md` and `LIFECYCLE.md` with centralized `scripts/` paths and deployment tool references.

## [1.2.0] - 2026-09-03
### Security
- **Path Traversal & Boundary Containment**: Enforced strict canonical path resolution (`is_safe_subpath`) and directory name regex validation across `restore_skills.py` and `sync.py`.
- **Symlink Protection**: Configured directory walkers and copying utilities (`shutil.copytree`, `shutil.copy2`) to prevent following unsafe external symbolic links (`symlinks=False`).
- **Safe Recursive Deletion Guards**: Protected destination deletion paths in `sync.py` to prevent accidental deletion outside the target root.
- **Secrets & Artifact Isolation**: Hardened `.gitignore` with comprehensive ignore patterns for credentials, private keys, certificates, environment files, SQLite databases, OS `.DS_Store` artifacts, backup files (`*.bak`), and scratch tools (`debug_*.py`).
- **Repository Hygiene & Pruning**: Removed stale backup files (`AGENTS.md.bak`, `director/SKILL.md.bak`), scratch scripts (`debug_scan.py`), and tracked OS metadata (`.DS_Store`).
- **Cross-Platform Path Portability**: Fixed hardcoded platform paths in `import_builtins.py` using dynamic home directory expansion (`os.path.expanduser`).
- **Resilient Manifest Parsing**: Added robust JSON parsing error handling in `deploy_skills.py`.
- **Architecture Decision Record**: Documented security decisions and STRIDE threat analysis in [ADR-0006](docs/adr/0006-repository-security-posture-hardening.md).

## [1.1.0] - 2026-08-28
### Fixed
- **Category Document Links**: Updated category index files to link directly to `SKILL.md` rather than the parent skill folder.
- **Frontmatter Parsing**: Enhanced `update_readme.py` frontmatter extraction with pure-Python fallback supporting multiline descriptions and block scalar types.

## [1.0.0] - 2025-05-20
### Added
- **Atomic vs. Composite Architecture**: Restructured the skills repository into "Atomic Skills" (building blocks) and "Composite Skills" (orchestrators).
- **Manifest-Driven Metadata**: Introduced `manifest.json` for all Composite skills to support multi-harness deployment.
- **Dependency Mapping**: Explicitly defined and documented dependencies for all Composite skills in their respective `SKILL.md` files.
- **Automated Deployment Pipeline**: Implemented `deploy_skills.py` to handle recursive dependency resolution and package generation for Pi, Gemini, and AI coding agent harnesses.
- **Comprehensive Documentation**: Added a project `README.md` and organized the `` directory for Atomic skills.
- **Audit Tracking**: Implemented `audit_status.json` to maintain a source of truth for skill categorization.

### Changed
- **Skill Organization**: Moved all Atomic skills into the `` directory.
- **Deployment Logic**: Added support for `deploy_package` generation.
