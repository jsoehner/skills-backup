# 0009. Production vs. Development Separation

## Status
Accepted

## Context
The repository serves as the comprehensive source of truth (Development) for all AI skills, but it contains a vast number of items that are not needed in every production environment. To maintain a lean and performant environment, we need to separate the "Source of Truth" from the "Production Environment."

## Decision
The `skills-backup/` directory (this repository) is designated as the **Source of Truth (Development)**. The `.pi/agent/skills` directory is designated as the **Production Environment**.
- **Source of Truth**: Contains every skill, every version, every ADR, and every management script.
- **Production Environment**: Contains only the subset of skills required for active use.

## Consequences
- **Positive**: Production environments remain lean; developers have a "sandbox" to experiment with new skills without affecting production.
- **Negative**: Requires a synchronization step to move/copy skills from the source of truth to production.
- **Required Actions**:
    - Use the `scripts/sync.py` and `scripts/restore_skills.py` scripts to manage the flow between these two environments.
    - Maintain `scripts/` in the source of truth to manage the distribution.
