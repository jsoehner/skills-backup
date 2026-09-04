# Changelog

## [1.2.0] - 2026-09-03
### Security
- **Path Traversal & Boundary Containment**: Enforced strict canonical path resolution (`is_safe_subpath`) and directory name regex validation across `restore_skills.py` and `sync.py`.
- **Symlink Protection**: Configured directory walkers and copying utilities (`shutil.copytree`, `shutil.copy2`) to prevent following unsafe external symbolic links (`symlinks=False`).
- **Safe Recursive Deletion Guards**: Protected destination deletion paths in `sync.py` to prevent accidental deletion outside the target root.
- **Secrets & Artifact Isolation**: Hardened `.gitignore` with comprehensive ignore patterns for credentials, private keys, certificates, environment files, SQLite databases, OS `.DS_Store` artifacts, backup files (`*.bak`), and scratch tools (`debug_*.py`).
- **Repository Hygiene & Pruning**: Removed stale backup files (`AGENTS.md.bak`, `director/SKILL.md.bak`), scratch scripts (`debug_scan.py`), and tracked OS metadata (`.DS_Store`).
- **Cross-Platform Path Portability**: Fixed hardcoded platform paths in `import_builtins.py` using dynamic home directory expansion (`os.path.expanduser`).
- **Resilient Manifest Parsing**: Added robust JSON parsing error handling in `deploy_skills.py`.
- **Architecture Decision Record**: Documented security decisions and STRIDE threat analysis in [ADR-0006](adr/0006-repository-security-posture-hardening.md).

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
