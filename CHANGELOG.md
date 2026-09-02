# Changelog

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
