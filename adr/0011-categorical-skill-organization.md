# 0011. Categorical Skill Organization

## Status
Accepted

## Context
As the number of skills grew to over 800, an alphabetical list became difficult to navigate. Developers struggled to quickly find skills related to specific domains (e.g., "Security" or "Data Engineering"). A more organized, categorical structure was needed to improve the developer experience (DX).

## Decision
Skills are now organized into a `skills/` subdirectory. The `README.md` file uses the `categories/` folder as the source of truth for skill categorization. This structure allows for:
1. **Categorical Grouping**: Skills are grouped by domain (e.g., AI, DevOps, Software Engineering).
2. **Documentation Linking**: Each category has a detailed documentation file in `categories/`.
3. **Scalability**: New categories and skills can be added without cluttering the root directory.

## Consequences
- **Positive**: Significantly improves discoverability and navigation; provides a cleaner repository structure.
- **Negative**: Requires updating all links in the `README.md` to point to the `skills/` subdirectory.
- **Required Actions**:
    - Ensure all skill folders are moved into the `skills/` directory.
    - Update the `README.md` category table and individual skill links.
    - Verify that `sync.py` and `restore_skills.py` handle the nested `skills/` directory correctly.
