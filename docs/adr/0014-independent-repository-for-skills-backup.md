# ADR 0014: Independent Repository for Skills Backup

## Context
The `skills-backup` directory has grown into a comprehensive source of truth for all AI skills, including metadata, scripts, and categorical organization. To improve maintainability, scalability, and isolation, it is best managed as a standalone repository rather than a subdirectory of a larger project.

## Decision
We will migrate `skills-backup` to its own dedicated GitHub repository: `jsoehner/skills-backup`.

## Rationale
- **Isolation**: Prevents the skills source of truth from being affected by changes in other projects.
- **Granular Permissions**: Allows for specific access controls for contributors to the skills library.
- **CI/CD Clarity**: Simplifies the setup of automated tests, documentation generation, and distribution pipelines specifically for skills.
- **Scalability**: Better handles the large number of files and subdirectories as the skill library continues to expand.

## Consequences
- **Positive**: Improved developer experience for skill contributors; cleaner project boundaries; easier versioning of the skills library.
- **Negative**: Requires a one-time migration of the repository and update of any existing hardcoded paths in other projects that pointed to the old location.
- **Mitigation**: We will provide clear instructions in the new repository's `README.md` on how to clone and use the skills, and we will update all internal documentation to point to the new URL.

## Status
Accepted
