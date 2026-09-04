# 0008. Hyphenated Naming Convention

## Status
Proposed

## Context
Inconsistent naming conventions (mixing hyphens and underscores) in skill names have caused friction with automated tooling and naming analyzers. It is necessary to establish a single, consistent standard for all skills within this repository to ensure compatibility with script automation and repository-wide search.

## Decision
All skill names must use hyphens (`-`) exclusively. Underscores (`_`) are strictly forbidden in skill names. This applies to the folder names in the `skills/` directory, the `SKILL.md` filenames, and any references within the documentation.

## Consequences
- **Positive**: Improves compatibility with automated scripts, simplifies regex-based searching, and ensures a consistent developer experience.
- **Negative**: Requires a one-time migration of all existing skill names and documentation references.
- **Required Actions**:
    - Rename all folders in `skills/` to use hyphens.
    - Update all `SKILL.md` filenames to use hyphens.
    - Audit and update all `README.md` and `SKILL.md` content to reflect the new names.
