# 0010. Management Script Centralization

## Status
Accepted

## Context
Previously, management scripts were scattered or located in various directories, making it difficult for developers to find tools for synchronization, restoration, and maintenance. This lack of centralization slowed down workflows and led to confusion about which scripts were the most up-to-date.

## Decision
All management scripts, automation tools, and maintenance utilities are moved to a dedicated `scripts/` directory at the root of the repository.

## Consequences
- **Positive**: Provides a single point of entry for all automation; improves discoverability; simplifies the `setup.sh` and `setup.ps1` scripts.
- **Negative**: Requires updating all documentation and user instructions to point to the new `scripts/` path.
- **Required Actions**:
    - Move all `.py` and `.sh` management scripts to `scripts/`.
    - Update `README.md` to reflect the new location.
    - Update `setup.sh` and `setup.ps1` to use the new paths.
