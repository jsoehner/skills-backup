---
name: "dependency-lifecycle-orchestrator"
description: "Orchestrates dependency management, including security audits, version upgrades, and lifecycle management."
version: 1
created: "2026-07-31"
updated: "2026-07-31"
metadata:
  model: inherit
dependencies:
  - dependency-management-deps-audit
  - dependency-updater
  - dependency-upgrade
---
## When to Use
Use for any task involving project dependencies, including security audits, version upgrades, and general dependency health management.

## Procedure
1. Identify the dependency task: Security Audit, Version Upgrade, or General Management.
2. For Security Audits: Use `dependency-security-audit` and `dependency-management-deps-audit` to scan for vulnerabilities and license issues.
3. For Version Upgrades: Use `dependency-updater` for safe updates and `dependency-upgrade` for major version transitions.
4. For General Management: Use `dependency-management-deps-audit` for ongoing health checks.
5. Synthesize the results into a clear action plan for the engineering team.

## Pitfalls
- Never perform major version upgrades without a staged rollout and full test suite.
- Ensure security audits are performed on every release candidate.
- Do not ignore 'dependency-updater' warnings for critical production packages.

## Verification
1. Dependency audit reports are generated and reviewed.
2. Version upgrades are tested and documented.
3. Project dependencies remain healthy and secure.