# 0013. Deploy Skills Root Path Resolution and Directory Traversal Hardening

## Status
Accepted

## Context
Following the centralization of management scripts into the `scripts/` directory (ADR-0010), `scripts/deploy_skills.py` evaluated its backup directory root using `os.path.dirname(os.path.abspath(__file__))`. Because the script now resided in `scripts/`, `BACKUP_DIR` pointed to `<repo>/scripts` rather than the repository root. This broke composite skill scanning (`manifest.json`) and packaging across the full catalog of skills located under the root and `skills/` directories.

Additionally:
1. Directory traversal during `os.walk` was descending into hidden directories and compiler caches (such as `__pycache__` and `.git`), degrading discovery performance and conflicting with repository hygiene standards established in ADR-0006.
2. The CLI lacked an option to specify or override the root skills directory, reducing flexibility for automated testing, CI/CD runners, and sub-tree deployments.

## Decision
We have updated `scripts/deploy_skills.py` with the following enhancements:
1. **Dynamic Repository Root Resolution**: Standardized `REPO_DIR` calculation to inspect `_SCRIPT_DIR`. If the parent folder name is `scripts`, it automatically resolves to the repository root (`os.path.dirname(_SCRIPT_DIR)`).
2. **In-Place Directory Pruning**: Modified `os.walk` traversal to filter directories in-place (`dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']`), eliminating unnecessary scanning into hidden directories and cache trees.
3. **CLI Root Directory Argument**: Added `--root-dir` parameter (defaulting to `REPO_DIR`) to the argument parser, enabling callers to specify custom root search paths.

## Consequences
- **Positive**: Restores full deployment planning and packaging capabilities for all supported AI harnesses (`pi`, `gemini`, `claude`); prevents wasteful walking through cache artifacts; supports customizable deployment roots for CI/CD and testing environments.
- **Negative**: None. Default CLI behavior remains backward-compatible with existing commands.
- **Required Actions**:
    - Update `docs/adr/README.md` index.
    - Update `CHANGELOG.md` with script fix and parameter enhancements.
    - Sync architectural record with the local memory capture system.

## Related ADRs
- [ADR-0006](0006-repository-security-posture-hardening.md): Repository Security Posture Assessment and Script Hardening
- [ADR-0010](0010-management-script-centralization.md): Management Script Centralization
