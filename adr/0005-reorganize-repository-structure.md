# 0005. Reorganize Repository Structure and Centralize Skills

## Status
Accepted

## Context
The repository previously had a fragmented structure with a redundant `skills-backup` folder and inconsistent script locations. This made it difficult for agents to reliably find the source of truth for skill definitions and management utilities. We needed a "Production vs. Development" separation where the root-level `skills/` folder serves as the lean production environment for the `.pi` and `.gemini` agents.

## Decision
We have reorganized the repository to the following structure:
- `skills/`: Contains all 465+ individual skill definitions.
- `scripts/`: Contains all management and automation scripts.
- `adr/`: Contains all Architectural Decision Records.
- `skill-groups/`: Contains categorical organization of skills.
- `config-skills/`: Contains configuration-specific templates.
- `docs/`: Contains general documentation.

We also standardized all skill names to a hyphenated convention (e.g., `ai-engineer` instead of `ai_engineer`) to ensure compatibility with automated tooling.

## Consequences
**Positive:**
- **Single Source of Truth**: Agents now have a predictable, flat structure for discovering skills.
- **Tooling Compatibility**: Hyphenated naming prevents issues with certain CLI tools and path parsers.
- **Discoverability**: The `skill-groups` directory provides a better developer experience for navigating the large skill set.

**Negative:**
- **Path Updates**: All existing scripts and documentation had to be updated to reflect the new relative paths.
- **Migration Effort**: Required a one-time cleanup of redundant folders and renaming of existing skill directories.
