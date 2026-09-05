# Developer Guide: Working with My Skills Repository

Welcome to the developer guide for the **My Skills Repository**. This guide provides the operational standards for maintaining and expanding our collection of AI skills.

## Repository Philosophy
This repository is the **Source of Truth**. All skills, ADRs, and management tools are housed here. We prioritize:
- **Hyphenated Naming**: Every skill must use hyphens (e.g., `skill-name`).
- **Categorical Organization**: Skills are grouped by domain for discoverability.
- **Manifest-Driven Deployment**: Use the `scripts/` directory to sync skills to production environments.

## Core Workflows

### 1. Adding a New Skill
To add a new skill to the repository:
1. **Define the Skill**: Create a new directory in `skills/` with a kebab-case name.
2. **Write Documentation**: Create a `SKILL.md` file inside that directory.
3. **Categorize**: Update the corresponding category file in `categories/`.
4. **Update Catalog**: Add the new skill to the table in `README.md`.
5. **Validate**: Run `python3 scripts/check_skills.py` to ensure the skill meets our standards.

### 2. Inspecting and Restoring Skills
To inspect what skills are installed vs new in your local environment, or to restore all skills:
```bash
# Check new vs installed skills
./setup.sh --status --client [pi|gemini|claude|opencode]

# Browse skills catalog
./setup.sh --catalog

# Inspect local memory system (OKF + ChromaDB)
./setup.sh --memory

# Restore all skills
./setup.sh --client [pi|gemini|claude|opencode]
```

On Windows PowerShell:
```powershell
.\setup.ps1 -Status -Client gemini
.\setup.ps1 -Catalog
.\setup.ps1 -Memory
.\setup.ps1 -Client gemini
```

### 3. Synchronizing to Production
To push or pull skills selectively using `scripts/sync.py`:
```bash
python3 scripts/sync.py deploy --client pi
python3 scripts/sync.py save --client pi
```

### 4. Managing Architectural Decisions
All significant technical changes must be documented as an Architectural Decision Record (ADR).
- Locate the next available number in `adr/`.
- Choose a template (Nygard, MADR, or Y-Statement).
- Document the **Context**, **Decision**, and **Consequences**.
- Commit the new ADR to the repository.

## Management Tools
All automation is located at repository root or in the `scripts/` directory:
- `setup.sh` / `setup.ps1`: Primary entry point for skill restoration, catalog exploration, and client status inspection.
- `scripts/catalog.py`: CLI and helper engine for catalog browsing and installation status checks.
- `scripts/restore_skills.py`: Rebuilds the production client environment from the source of truth.
- `scripts/sync.py`: Bidirectionally synchronizes specific skill subsets between repo and client.
- `scripts/update_readme.py`: Automatically generates and updates `README.md` and `categories/*.md` catalogs.

## Standards & Compliance
- **ADR 0008**: Strictly enforces hyphenated naming.
- **ADR 0009**: Ensures separation between the `skills-backup` (Source of Truth) and `.pi/agent/skills` (Production).
- **ADR 0011**: Ensures the `categories/` folder remains the source of truth for the `README.md` catalog.

---
*For more details, refer to the full list of Architectural Decision Records in the `adr/` directory.*
