---
name: repo-governance-automation
group: software_architecture
description: "Automates the application of a 'Gold Standard' governance suite to any GitHub repository, systematically injecting documentation, DX, workflows, and security configurations to improve maintainability and security."
---

# Repository Governance Automation Skill

This skill automates the application of a "Gold Standard" governance suite to any GitHub repository. When invoked with a list of repository URLs, the skill will systematically inject the following files and configurations to improve developer experience, security, and maintainability.

## Applied Governance Suite

The following files are created/updated in each target repository:

### 1. Documentation & DX
- **`CONTRIBUTING.md`**: Standardized guidelines for contributors, including setup instructions, branching strategies, and commit standards.
- **`PULL_REQUEST_TEMPLATE.md`**: A structured template for all PRs to ensure clear descriptions, testing evidence, and checklists.

### 2. Workflow & Automation
- **`commit-lint.yml`**: A GitHub Action that enforces **Conventional Commits** (e.g., `feat:`, `fix:`) on all pushes and PRs.
- **`changelog.yml`**: A GitHub Action that automatically generates a `CHANGELOG.md` based on the Conventional Commit history.
- **`sbom.yml`**: A GitHub Action that generates Software Bill of Materials (SBOM) in both **CycloneDX** and **SPDX** standard JSON formats via Anchore / Syft, automatically archiving artifacts and attaching them to release tags.

### 3. Security & Supply Chain
- **`security-testing.yml`**: A multi-layered security pipeline that runs:
    - **Gitleaks**: To detect hardcoded secrets.
    - **Trivy**: To scan container images for vulnerabilities.
    - **Semgrep**: To perform Static Application Security Testing (SAST) on the source code.
- **`github-actions-node24` & Security Pinning**: All injected and existing GitHub workflows are audited and updated according to the [`github-actions-node24`](../github-actions-node24/SKILL.md) skill to prevent Node 20 deprecation warnings, enforce SHA commit pinning against supply chain poisoning, and ensure Node 24 runtime support.
- **`security-scanning-security-dependencies`**: For deep supply chain audits and vulnerability remediation roadmaps, refer to the [`security-scanning-security-dependencies`](../security-scanning-security-dependencies/SKILL.md) skill.

## Usage

Provide a list of repository URLs. The skill will iterate through them and apply the suite.

**Example Input:**
`["https://github.com/user/repo1", "https://github.com/user/repo2"]`

## Implementation Logic
The skill uses the following templates for file generation:

- **PR Template**: Standardized across all projects.
- **Contributing Guide**: Adaptive to the project's primary tech stack (Python, JS/TS, Kotlin, etc.).
- **Security Workflow**: Configured with standard thresholds (Critical/High) and standard paths.
- **SBOM Workflow (`sbom.yml`)**: Generates CycloneDX & SPDX JSON artifacts, publishes build artifacts, and attaches them to releases.
- **Node 24 Upgrade Policy**: Enforces [`github-actions-node24`](../github-actions-node24/SKILL.md) standards:
  - Bumps all GitHub Actions to Node 24 compatible major versions (e.g. `actions/checkout@v7`, `actions/upload-artifact@v4`, `softprops/action-gh-release@v3`).
  - Enforces immutable 40-character commit SHA pinning on all workflow `uses:` directives.
