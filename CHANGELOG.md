# Changelog

## [1.2.0] - 2026-09-02
### Changed
- **Directory Structure**: Renamed `tools/` directory to `skills/` to standardize the skill repository naming.
- **Documentation & Scripts**: Updated all documentation (`README.md`, `CONTRIBUTING.md`, `LIFECYCLE.md`), `audit_status.json`, and utilities (`deploy_skills.py`, `debug_scan.py`, `sync.py`, `restore_skills.py`, `update_readme.py`) to reference `skills/`.

## [1.1.0] - 2026-08-28
### Fixed
- **Category Document Links**: Updated category index files to link directly to `SKILL.md` rather than the parent skill folder.
- **Frontmatter Parsing**: Enhanced `update_readme.py` frontmatter extraction with pure-Python fallback supporting multiline descriptions and block scalar types.

## [1.0.0] - 2025-05-20
### Added
- **Atomic vs. Composite Architecture**: Restructured the skills repository into "Atomic Skills" (building blocks) and "Composite Skills" (orchestrators).
- **Manifest-Driven Metadata**: Introduced `manifest.json` for all Composite skills to support multi-harness deployment.
- **Dependency Mapping**: Explicitly defined and documented dependencies for all Composite skills in their respective `SKILL.md` files.
- **Automated Deployment Pipeline**: Implemented `deploy_skills.py` to handle recursive dependency resolution and package generation for Pi, Gemini, and Claude Code harnesses.
- **Comprehensive Documentation**: Added a project `README.md` and organized the `tools/` directory for Atomic skills.
- **Audit Tracking**: Implemented `audit_status.json` to maintain a source of truth for skill categorization.

### Changed
- **Skill Organization**: Moved all Atomic skills into the `tools/` directory.
- **Deployment Logic**: Added support for `deploy_package` generation.
