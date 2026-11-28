# My Skills Repository

[![Build Verification](https://img.shields.io/badge/Build%20Verification-Verified%202026--11--20-brightgreen)](docs/BUILD_VERIFICATION.md)

This repository is a comprehensive collection of AI "skills" designed for various AI harnesses, including Pi-agent, Gemini, and AI coding agent.

> **Build Verification:** Last functionally verified on `2026-11-20` by **Jeffs' Automated build and deploy agent** — see [docs/BUILD_VERIFICATION.md](docs/BUILD_VERIFICATION.md).

## Architecture

We use a dual-layered architecture to distinguish between fundamental building blocks and complex workflows:

### 1. Atomic Skills
**Location**: `skills/`
Atomic skills are self-contained, modular components. They do not depend on other skills within this repository. Examples include:
- `bash-pro`: Expert shell scripting.
- `python-pro`: Advanced Python development.
- `sql-pro`: SQL optimization and schema design.

### 2. Composite Skills
**Location**: Root directory (`yuv-skills-backup/`)
Composite skills are orchestrators or complex workflows that require one or more Atomic or other Composite skills to function.
- **Dependencies**: Each Composite skill includes a `manifest.json` file and explicitly lists its dependencies in its `SKILL.md` file.
- **Examples**:
    - `yuv-pilot`: The top-level orchestrator for YUV.AI brand work.
    - `ai-engineer`: A comprehensive suite for building LLM applications.
    - `video-edit`: A workflow for creating captioned showcase videos.

## Quick Start & Setup

The repository provides cross-platform setup scripts for restoring skills, inspecting status, and exploring the catalog.

### Setup & Installation
```bash
# Bash (macOS/Linux)
./setup.sh --client pi        # Restores to ~/.pi/agent/skills
./setup.sh --client gemini    # Restores to ~/.gemini/config/skills
./setup.sh --client claude    # Restores to ~/.claude/skills
./setup.sh --client opencode  # Restores to ~/.opencode/skills
./setup.sh --client hermes    # Restores to $LOCALAPPDATA/hermes/skills (or ~/.local/share/hermes/skills)

# Preview or clean restore / back up local client skills (including new skills)
./setup.sh --client gemini --dry-run
./setup.sh --client gemini --clean
./setup.sh --backup --client pi --dry-run
```

```powershell
# Windows PowerShell
.\setup.ps1 -Client pi
.\setup.ps1 -Client gemini
.\setup.ps1 -Client claude
.\setup.ps1 -Client opencode
.\setup.ps1 -Client hermes

# Preview or clean restore / back up local client skills (including new skills)
.\setup.ps1 -Client gemini -DryRun
.\setup.ps1 -Client gemini -Clean
.\setup.ps1 -Backup -Client pi -DryRun
```

### Inspect New vs. Existing Skills
Check which skills in the repository are already installed versus new/uninstalled in your local environment:
```bash
./setup.sh --status --client gemini     # Full status comparison
./setup.sh --new --client gemini        # List only new skills available
./setup.sh --installed --client gemini  # List only existing/installed skills
```

### Browse Skill Catalog
Explore available skills with descriptions, categories, and keyword search:
```bash
./setup.sh --catalog                    # Full catalog by category
./setup.sh --catalog -g databases_data  # Filter by category
./setup.sh --catalog -q postgres        # Search skills by keyword
./setup.sh --categories                 # List all categories and counts
```

### Inspect Local Memory System
Inspect host directories, RAG storage presence, search stored policies/context, and inspect full memory documents:
```bash
./setup.sh --memory                     # Inspect memory status and list stored OKF & ChromaDB records
./setup.sh --memory -q <keyword>        # Search stored memories across policies and vector contexts
./setup.sh --memory --details           # Display full document contents for memory items
python3 scripts/inspect_memory.py --json # Export structured JSON for agent harnesses
```

```powershell
.\setup.ps1 -Memory                     # Windows PowerShell
.\setup.ps1 -Memory -Search <keyword>   # Search stored memories
.\setup.ps1 -Memory -Details            # Display full document contents
```

### Agent Pre-Flight Briefing & Fork Guardrail
Retrieve applicable organizational policies and lessons learned, and verify fork safety before planning or applying code modifications:
```bash
./setup.sh --preflight                  # Run agent pre-flight briefing (fork status + OKF policies + ChromaDB context)
./setup.sh --preflight <target_path>    # Run pre-flight briefing on a specific repository
./setup.sh --check-fork <target_path>   # Verify if repository is an active fork before modifying
python3 scripts/inspect_memory.py --preflight .
python3 scripts/check_fork_guardrail.py .
```

```powershell
.\setup.ps1 -Preflight                  # Windows PowerShell pre-flight briefing
.\setup.ps1 -Preflight -TargetPath <target_path>
.\setup.ps1 -CheckFork                  # Fork origin and upstream sync check
```

## Deployment & Synchronization

The repository provides multi-tiered deployment workflows ranging from automated one-command client installation to bidirectional synchronization and manifest-driven composite packaging.

### 1. Supported Target Runtimes

All skills are automatically flattened and deployed directly into each client's canonical skill directory:

| Client Runtime | Target Directory | CLI Flag | Description |
|---|---|---|---|
| **Pi Agent** | `~/.pi/agent/skills` | `pi` | Default local lightweight agent runtime |
| **Gemini CLI** | `~/.gemini/config/skills` | `gemini` | Google DeepMind Gemini agent harness |
| **Claude Code** | `~/.claude/skills` | `claude` | Anthropic Claude agent skill directory |
| **OpenCode** | `~/.opencode/skills` | `opencode` | OpenCode community runtime |

---

### 2. Quick Deployment & Environment Restoration

The primary deployment method restores and flattens all repository skills into your target client with automatic directory creation and path containment checks:

#### Automated CLI Scripts (Recommended)
```bash
# macOS / Linux (Bash)
./setup.sh --client gemini      # Deploy/restore all skills to Gemini
./setup.sh --client pi          # Deploy/restore all skills to Pi
./setup.sh --client claude      # Deploy/restore all skills to Claude
./setup.sh --client opencode    # Deploy/restore all skills to OpenCode
```

```powershell
# Windows PowerShell
.\setup.ps1 -Client gemini      # Deploy/restore all skills to Gemini
.\setup.ps1 -Client pi          # Deploy/restore all skills to Pi
.\setup.ps1 -Client claude      # Deploy/restore all skills to Claude
.\setup.ps1 -Client opencode    # Deploy/restore all skills to OpenCode
```

#### Direct Python Restoration
```bash
python3 scripts/restore_skills.py . --client gemini
```

**Deployment Guarantees:**
- **Flattening**: Eliminates nested directories. All skills reside strictly at the top level of the target client's skills folder.
- **Path Containment & Security**: Enforces `is_safe_subpath` checks and blocks symlink traversal to prevent directory escape attacks.
- **Client Customization Preservation**: Existing client-only skills not tracked in the repository are preserved and never deleted.

---

### 3. Bidirectional Environment Synchronization

When authoring or modifying skills directly within an active agent environment, use `scripts/sync.py` to keep your local client and the repository in sync:

```bash
# Deploy changes from repository to agent client
python3 scripts/sync.py deploy --client gemini

# Save new/edited skills from agent client back into the repository
python3 scripts/sync.py save --client gemini
```

- **`deploy`**: Copies updated skills from `skills/` and `config-skills/` into the client environment.
- **`save`**: Discovers new or edited skills in the client directory, automatically determines their category via frontmatter analysis, and copies them back into the proper repository folder.

---

### 4. Manifest-Driven Composite Deployment

For complex, multi-skill workflows, `scripts/deploy_skills.py` provides manifest-based dependency resolution and deployment planning:

```bash
# Plan and preview dependencies for a specific harness
python3 scripts/deploy_skills.py --harness pi --dry-run

# Generate the deployment package
python3 scripts/deploy_skills.py --harness gemini
```

- **Recursive Dependency Resolution**: Inspects `manifest.json` files in composite skills and automatically includes all dependent atomic tools.
- **Target Packaging**: Generates a self-contained deployment package ready for air-gapped or containerized distribution.

---

### 5. Pre-Flight Inspection & Verification

Before and after deploying, verify the deployment status across your runtimes:

```bash
./setup.sh --status --client gemini     # Compare repository vs installed skills
./setup.sh --new --client gemini        # View only uninstalled / new skills
./setup.sh --installed --client gemini  # View only currently active skills
```

## Project Structure
- `skills/`: User skills categorized by domain.
- `config-skills/`: System configuration skills.
- `categories/`: Dynamic markdown catalog per category.
- `docs/`: Technical documentation and architecture records.
  - `docs/adr/`: Architecture Decision Records (ADRs) and Governance Strategy.
- `scripts/`:
  - `restore_skills.py`: Core restoration logic and governance sync for agent clients.
  - `catalog.py`: Skills catalog engine and status inspector.
  - `check_fork_guardrail.py`: Fork origin verification, upstream status, and sync availability guardrail.
  - `inspect_memory.py`: Pre-flight memory briefing (OKF policies & ChromaDB lessons learned) and memory explorer.
  - `sync.py`: Selective bidirectional synchronization.
  - `update_readme.py`: Catalog and documentation generator.
  - `deploy_skills.py`: Manifest-driven deployment packager.
- `setup.sh`: Bash setup, status check, and catalog CLI.
- `setup.ps1`: Windows PowerShell setup, status check, and catalog CLI.
- `manifest.json`: Machine-readable metadata for Composite skills.
- `audit_status.json`: Tracks the categorization and migration status of all skills.
- `CHANGELOG.md`: History of updates and new skills.
- `SKILL.md`: Documentation for every individual skill.

## Contributing

To add a new skill:
1. Determine if it is **Atomic** (add to `skills/`) or **Composite** (add to root).
2. Create a `SKILL.md` file describing the skill.
3. If Composite, create a `manifest.json` and list dependencies.
4. Update `audit_status.json` to reflect the new skill.
5. Run `python3 scripts/update_readme.py` to update the catalog documentation.

## 🔗 Composite Pipeline Orchestrators & Governance Decision Matrix

This repository provides single-call pipeline orchestrators designed to trigger complete, multi-stage workflows across dependent skills. When an agent harness executes one of these grouped skills, each dependent skill is triggered in strict sequential order, passing outputs, reports, and artifacts down the chain.

Use this unified decision matrix to identify the right composite skill, its triggering conditions, execution flow, and delivered artifacts:

| Orchestrator Skill | Category / Domain | When to Invoke (Trigger) | Sequential Workflow & Core Actions | Output Artifacts & Enforced Guardrails |
|---|---|---|---|---|
| [`repo-governance-orchestrator`](skills/repo-governance-orchestrator/SKILL.md) | Repository Scaffolding & Supply Chain DX | New repo setup, batch standardizing repo DX, or scaffolding dual-engine BOM/CBOM scanning | Injects Gold Standard governance suite (`CONTRIBUTING.md`, `PULL_REQUEST_TEMPLATE.md`, `commit-lint.yml`, dual-engine `sbom.yml`, `security-testing.yml`, Node 24 SHA pinning) | Standardized Repo Governance Suite $\rightarrow$ CycloneDX & SPDX SBOMs $\rightarrow$ CycloneDX CBOM & AST Reconciliation $\rightarrow$ CI Test Verification $\rightarrow$ PQC Scorecard |
| [`security-governance-orchestrator`](skills/security-governance-orchestrator/SKILL.md) | Security & Compliance | Onboarding to SOC2/OWASP/CIS, setting up PR security gates, or establishing repository security policies | Executes 6-phase SDLC security lifecycle: STRIDE threat modeling $\rightarrow$ SecADRs $\rightarrow$ SARIF SAST/CVE scans $\rightarrow$ Dependabot 7-day cooldowns $\rightarrow$ pre-commit hooks | `security-governance.yml`, `dependabot.yml`, `Security_ADR_Template.md`, `adr_security_gatekeeper.py`, `pre_commit.py`, `SECURITY_POSTURE.md` & Memory Sync |
| [`security-audit-orchestrator`](skills/security-audit-orchestrator/SKILL.md) | Security Assessment | Pre-deployment security audits, periodic compliance assessments, or vulnerability discovery | Scans repo for vulnerabilities, builds attack trees, runs memory forensics, and compiles findings | Threat model matrix, SAST scans, forensic analysis report, unified vulnerability report with CVSS ratings |
| [`security-agent-orchestrator`](skills/security-agent-orchestrator/SKILL.md) | Security Remediation | Fixing known security vulnerabilities, hardening endpoints, or implementing secure auth flows | Derives mitigations from threat models, writes hardened code, patches dependencies, and verifies with SAST | Hardened source files, patch diffs, sanitized input handlers, compliance verification report |
| [`architecture-governance-orchestrator`](skills/architecture-governance-orchestrator/SKILL.md) | Macro Architecture Governance | Architectural redesign, multi-cloud migrations, or establishing macro-level design consistency | Generates visual C4 models, formulates cloud/K8s/monorepo blueprints, and links decisions to ADRs | C4 Context/Container/Component diagrams, cloud/K8s infrastructure blueprints, ADR alignment matrix, OKF policy sync |
| [`adr-governance-orchestrator`](skills/adr-governance-orchestrator/SKILL.md) | Decision Lifecycle Governance | Making significant architectural choices, superseding decisions, or auditing decision records | Auto-provisions `docs/adr/`, checks for overlapping decisions, drafts MADR/Nygard templates, and enforces gatekeeping | Validated ADRs (`docs/adr/`), updated index (`docs/adr/README.md`), gatekeeper compliance logs, OKF policy sync |
| [`c4-modeling-pipeline`](skills/c4-modeling-pipeline/SKILL.md) | Architecture Reverse-Engineering | Documenting existing or legacy systems lacking architectural documentation | Analyzes code structure bottom-up: Code $\rightarrow$ Component $\rightarrow$ Container $\rightarrow$ Context $\rightarrow$ ADR linkage | Complete C4 Mermaid diagrams, system boundary documentation, initial ADR catalog |
| [`dependency-lifecycle-orchestrator`](skills/dependency-lifecycle-orchestrator/SKILL.md) | Strategic Dependency Governance | Auditing library vulnerabilities, evaluating licenses, or planning complex framework upgrades | Audits dependencies, assesses breaking changes, and formulates staged upgrade and rollback roadmaps | Dependency health report, CVE vulnerability list, staged migration & rollback plan |
| [`dependency-release-pipeline`](skills/dependency-release-pipeline/SKILL.md) | Dependency Release Execution | Executing verified dependency bumps and publishing changelog entries | Upgrades packages, regenerates lockfiles, executes test suites, and opens comprehensive PRs | Updated lockfiles & migrated syntax, passing test logs, enhanced PR description, `CHANGELOG.md` entry |
| [`conductor-pipeline-orchestrator`](skills/conductor-pipeline-orchestrator/SKILL.md) | Context-Driven Development | Driving structured multi-phase feature development via Conductor methodology | Scaffolds product context, writes `spec.md` & `plan.md`, executes TDD cycles, and records phase checkpoints | `conductor/` tracks, task-level verified git commits, track status registries |
| [`tdd-pipeline-orchestrator`](skills/tdd-pipeline-orchestrator/SKILL.md) | Test-Driven Development | Writing reliable features or bug fixes following strict Red-Green-Refactor cycles | Writes failing test suites (Red), implements minimal passing code (Green), and refactors for quality (Refactor) | Unit/integration test suites, minimal clean implementation, refactored production code |
| [`incident-diagnostics-pipeline`](skills/incident-diagnostics-pipeline/SKILL.md) | Production Incident Triage | Live production incidents, recurring bug reports, or post-incident reviews | Correlates telemetry/logs, constructs minimal reproduction test, implements fix, and writes postmortem | RCA document, reproduction test case, verified code fix, blameless postmortem |
| [`error-diagnostics-orchestrator`](skills/error-diagnostics-orchestrator/SKILL.md) | Error Diagnostics & Resilience | Systematic error debugging, root cause analysis, and resilient exception handling | Failure analysis $\rightarrow$ Telemetry & distributed tracing $\rightarrow$ Multi-agent review $\rightarrow$ Resilient error-handling patterns | Root Cause Analysis (RCA), distributed trace map, multi-perspective review notes, hardened error handling code |
| [`performance-optimization-orchestrator`](skills/performance-optimization-orchestrator/SKILL.md) | Full-Stack Performance Tuning | Profiling and resolving latency, query, memory, or throughput bottlenecks across stack | Multi-tier performance optimization: SQL queries $\rightarrow$ Spark job partitioning/shuffles $\rightarrow$ Vector index tuning (HNSW) $\rightarrow$ Application runtime profiling | Optimized SQL queries, tuned Spark DAGs, benchmarked vector indices, profiling bottleneck reports |
| [`content-governance-orchestrator`](skills/content-governance-orchestrator/SKILL.md) | Multi-Format Content Governance | Multi-modal content delivery and technical documentation authoring | Multi-modal content delivery: Technical documentation $\rightarrow$ Office documents (PDF/DOCX/PPTX/XLSX) $\rightarrow$ E-E-A-T & SEO quality governance | Technical tutorials & reference guides, formatted office documents, E-E-A-T audit & structured schema |
| [`data-platform-orchestrator`](skills/data-platform-orchestrator/SKILL.md) | Data Platform & Engineering | End-to-end data engineering, data modeling, and validation pipeline setup | End-to-end data engineering: Database schema design $\rightarrow$ dbt model transformations $\rightarrow$ Data quality testing $\rightarrow$ Analytical optimization | Database schema DDL, dbt transformation models, data quality test suites, validation reports |
| [`mlops-pipeline-orchestrator`](skills/mlops-pipeline-orchestrator/SKILL.md) | Production MLOps Lifecycle | Moving machine learning pipelines from training into production serving and observability | Production ML lifecycle: Model training $\rightarrow$ Deployment packaging & serving config $\rightarrow$ Drift monitoring & alerts | Model training artifacts, deployment configuration, drift detection rules, monitoring alerts |
| [`frontend-design-system-orchestrator`](skills/frontend-design-system-orchestrator/SKILL.md) | Frontend & Design Systems | Scaffolding, standardizing, and validating design tokens and UI components | UI/UX and design system consistency: UX design alignment $\rightarrow$ Design tokens $\rightarrow$ Accessible React components $\rightarrow$ Visual validation | Design tokens, accessible React components, visual validation test reports |
| [`video-brand-pipeline-orchestrator`](skills/video-brand-pipeline-orchestrator/SKILL.md) | Video Branding & Social Content | Production of viral short-form videos and branded landing pages | Video downloading, brand design tokens, motion editing, viral shorts, and hero landing pages | Raw media & audio stem, brand visual tokens, edited video with kinetic captions, vertical viral MP4, scroll-driven hero landing page |
| [`multimedia-production-orchestrator`](skills/multimedia-production-orchestrator/SKILL.md) | End-to-End Multimedia Production | Multi-channel media production across video, HyperFrames, and web | Multimedia production: Download $\rightarrow$ Brand $\rightarrow$ Edit $\rightarrow$ Render $\rightarrow$ Landing Page | Raw media, brand tokens, edited video, HyperFrames compositions, published landing page |
| [`seo-content-pipeline`](skills/seo-content-pipeline/SKILL.md) | SEO Content & SERP Dominance | Planning, drafting, and optimizing high-ranking organic search content | Keyword strategy, article writing, structural/schema optimization, snippet formatting, and E-E-A-T auditing | Article outline & search intent, keyword density & LSI matrix, draft Markdown copy, heading hierarchy & schema, meta titles & snippet blocks, E-E-A-T audit scorecard |
| [`feature-delivery-pipeline`](skills/feature-delivery-pipeline/SKILL.md) | Full-Stack Feature Delivery | Multi-phase contract-driven full-stack feature delivery | Contract-driven full-stack delivery: Database schema $\rightarrow$ API contracts $\rightarrow$ Frontend hierarchy $\rightarrow$ Implementation $\rightarrow$ E2E tests | Database schema & migrations, OpenAPI/GraphQL contracts, component tree & API client, integrated full-stack code, passing E2E test report |
| [`startup-strategy-orchestrator`](skills/startup-strategy-orchestrator/SKILL.md) | Startup Strategy & Financial Modeling | Startup planning, headcount modeling, and investor-ready business case generation | Startup planning and financial modeling: Market opportunity $\rightarrow$ Financial projections $\rightarrow$ Headcount & operations $\rightarrow$ Synthesis | Market sizing, financial model, headcount plan, executive business case |
| [`startup-business-pipeline`](skills/startup-business-pipeline/SKILL.md) | Investor Opportunity Pipeline | Comprehensive startup market sizing, unit economics, and pitch packaging | Market sizing (TAM/SAM/SOM), opportunity analysis, headcount planning, 3-5y financials, competitive analysis, and investor business case | TAM/SAM/SOM calculations, customer ICP & opportunity analysis, phased headcount model, 3-5 year financial forecast, competitive matrix, investor-ready business case |

## 🛡️ Repository Governance & Composite Orchestrator Taxonomy

As a codebase evolves, different governance needs arise at different points in the software development lifecycle (SDLC). To prevent overlap and clarify tool selection, the repository organizes composite skills into dedicated functional tiers.

### How Composite Skills Differ: Deep Dive & Comparison

#### 1. Baseline Scaffolding vs. Continuous Security Governance

| Dimension | [`repo-governance-orchestrator`](skills/repo-governance-orchestrator/SKILL.md) | [`security-governance-orchestrator`](skills/security-governance-orchestrator/SKILL.md) |
|---|---|---|
| **Primary Scope** | **Developer Experience (DX) & CI/CD Scaffolding** | **Institutional Security Posture & Compliance Gatekeeping** |
| **Operational Mode** | Batch initializer / setup script across target repos. | Continuous SDLC policy enforcement, threat modeling, and PR gatekeeping. |
| **Injected Assets** | `CONTRIBUTING.md`, `PULL_REQUEST_TEMPLATE.md`, `commit-lint.yml`, `sbom.yml`, baseline `security-testing.yml`, Node 24 SHA pinning. | STRIDE threat models, Security ADRs (`Security_ADR_Template.md`), `security-governance.yml` with SARIF upload, Dependabot 7-day cooldowns, pre-commit git hooks (`pre_commit.py`), and `adr_security_gatekeeper.py`. |
| **When to Use** | Bootstrapping a new repository or retrofitting a fleet of repos with standard contribution guides, commit linting, and basic SBOM/SAST workflows. | Onboarding repos to organizational security compliance (SOC2/OWASP/CIS), authoring security ADRs, or blocking PRs that bypass security architecture reviews. |

#### 2. Security Governance vs. Security Auditing vs. Security Remediation

| Dimension | [`security-governance-orchestrator`](skills/security-governance-orchestrator/SKILL.md) | [`security-audit-orchestrator`](skills/security-audit-orchestrator/SKILL.md) | [`security-agent-orchestrator`](skills/security-agent-orchestrator/SKILL.md) |
|---|---|---|---|
| **Primary Role** | **Policy & Gatekeeping Orchestrator** | **Forensic & Vulnerability Diagnostic** | **Hands-On Code Remediation Engine** |
| **Execution Trigger** | Establishing institutional guardrails, PR gatekeeper checks, or compliance onboarding. | Periodic security review, pre-audit assessment, or incident investigation. | Active vulnerability remediation sprint, fixing flagged SAST/CVE issues in code. |
| **Modifies Code?** | Configures workflows, hooks, ADR templates, and policies. | **No** (read-only audit, scans, and forensic inspection). | **Yes** (modifies source code, sanitizes inputs, hardens endpoints, patches deps). |
| **Key Deliverable** | CI/CD gatekeeper scripts, Dependabot cooldown, pre-commit hooks, `SECURITY_POSTURE.md`. | Comprehensive vulnerability & forensic audit report with CVSS severity ratings. | Hardened source files, passing SAST regression suite, and verified compliance certificate. |

#### 3. Macro Architecture vs. ADR Lifecycle Management

| Dimension | [`architecture-governance-orchestrator`](skills/architecture-governance-orchestrator/SKILL.md) | [`adr-governance-orchestrator`](skills/adr-governance-orchestrator/SKILL.md) | [`c4-modeling-pipeline`](skills/c4-modeling-pipeline/SKILL.md) |
|---|---|---|---|
| **Primary Scope** | **Macro-Level System Topology & Strategy** | **Micro-Level Decision Record Integrity** | **Bottom-Up Architecture Reverse-Engineering** |
| **Core Function** | Visualizes system boundaries, cloud/K8s blueprints, monorepo structures, and links to ADRs. | Manages the full lifecycle of ADRs: template choice (MADR/Nygard), gatekeeping compliance, indexing, and superseding. | Scans existing codebases bottom-up (Code $\rightarrow$ Component $\rightarrow$ Container $\rightarrow$ Context) to synthesize architecture models. |
| **When to Use** | Designing a new distributed system, refactoring across cloud providers, or aligning monorepo boundaries. | Recording a significant technical decision (e.g. database choice, auth provider, protocol change). | Documenting or onboarding onto an undocumented legacy codebase to produce C4 diagrams. |
| **Gatekeeper** | Validates consistency between cloud architecture, K8s manifests, and codebase structure. | Enforces strict ADR standards via `adr-gatekeeper` (unique IDs, consequences, non-deletion, memory sync). | Verifies component and container diagrams against physical package imports. |

#### 4. Dependency Governance vs. Dependency Release Execution

| Dimension | [`dependency-lifecycle-orchestrator`](skills/dependency-lifecycle-orchestrator/SKILL.md) | [`dependency-release-pipeline`](skills/dependency-release-pipeline/SKILL.md) |
|---|---|---|
| **Primary Scope** | **Strategic Dependency Health & Upgrade Planning** | **Tactical Upgrade Execution & Release Publishing** |
| **Core Function** | Scans dependencies for CVEs, license conflicts, breaking change impacts, and creates staged rollout plans. | Bumps versions, updates lockfiles, runs unit/integration tests, authors enhanced PRs, and updates `CHANGELOG.md`. |
| **When to Use** | Assessing dependency risks across a repository, evaluating library health, or planning major framework upgrades. | Executing the actual version bump PR, verifying tests pass, and generating the release changelog entry. |

#### 5. Diagnostics, Performance, and Content Governance

- **[`error-diagnostics-orchestrator`](skills/error-diagnostics-orchestrator/SKILL.md)**: Coordinates error analysis, distributed tracing, and multi-agent reviews to isolate root causes and formulate resilient error-handling patterns.
- **[`incident-diagnostics-pipeline`](skills/incident-diagnostics-pipeline/SKILL.md)**: The end-to-end incident response lifecycle—correlates telemetry, reproduces bugs via test cases, deploys verified code fixes, and writes blameless postmortems.
- **[`performance-optimization-orchestrator`](skills/performance-optimization-orchestrator/SKILL.md)**: Coordinates performance profiling across SQL queries, Spark jobs, vector index tuning (HNSW/IVF), and CPU/memory bottlenecks.
- **[`content-governance-orchestrator`](skills/content-governance-orchestrator/SKILL.md)**: Governs multi-format technical documentation (tutorials, references, API guides) and office document generation (PDF, DOCX, PPTX, XLSX) while enforcing E-E-A-T and style rules.

---

### 🌳 Decision Tree: Choosing the Right Governance Skill

```mermaid
flowchart TD
    Start["🎯 What is your primary objective?"] --> Objective{Select Need}

    Objective -->|"Scaffold new repo DX, baseline CI & BOMs"| RepoGov["🚀 repo-governance-orchestrator<br/>(Inject CONTRIBUTING, PR template, commit-lint, dual-engine SBOM/CBOM, Node 24 SHA pinning)"]

    Objective -->|"Security & Compliance"| SecBranch{Action Type?}
    SecBranch -->|"Institutional policy, PR gates & SecADRs"| SecGov["🔒 security-governance-orchestrator<br/>(STRIDE, SecADRs, SARIF CI, pre-commit hooks, Dependabot cooldown)"]
    SecBranch -->|"Investigative vulnerability assessment"| SecAudit["🔍 security-audit-orchestrator<br/>(Forensic scans, attack trees, vulnerability report)"]
    SecBranch -->|"Patch vulnerabilities & write secure code"| SecRemed["🛡️ security-agent-orchestrator<br/>(Mitigation mapping, code hardening, regression verification)"]

    Objective -->|"System Architecture & Decisions"| ArchBranch{Focus Area?}
    ArchBranch -->|"System topology & C4 visual models"| ArchGov["🏗️ architecture-governance-orchestrator<br/>(C4 diagrams, cloud/K8s/monorepo blueprints)"]
    ArchBranch -->|"Formal decision record lifecycle"| AdrGov["📜 adr-governance-orchestrator<br/>(MADR templates, adr-gatekeeper validation, registry index, OKF sync)"]
    ArchBranch -->|"Reverse-engineer legacy system C4"| C4Pipe["🗺️ c4-modeling-pipeline<br/>(Bottom-up Code → Component → Container → Context)"]

    Objective -->|"Dependencies & Releases"| DepBranch{Action Type?}
    DepBranch -->|"Audit CVEs & plan major upgrades"| DepLife["📦 dependency-lifecycle-orchestrator<br/>(CVE/license audit, compatibility matrix, upgrade roadmap)"]
    DepBranch -->|"Execute package bumps & changelogs"| DepRel["🚀 dependency-release-pipeline<br/>(Lockfile updates, test pass, enhanced PR, CHANGELOG.md)"]

    Objective -->|"Operational Triage & Performance"| OpsBranch{Focus Area?}
    OpsBranch -->|"Root cause analysis & fix patterns"| ErrDiag["🩺 error-diagnostics-orchestrator<br/>(Trace correlation, multi-agent review, resilient handling)"]
    OpsBranch -->|"End-to-end incident fix & postmortem"| IncDiag["🚨 incident-diagnostics-pipeline<br/>(Reproduction test, verified fix, blameless postmortem)"]
    OpsBranch -->|"SQL / Spark / Vector tuning"| PerfOpt["⚡ performance-optimization-orchestrator<br/>(SQL tuning, Spark shuffles, HNSW indexing, profiling)"]
```


## 🧠 Local Memory RAG Architecture & Token Flow

The repository integrates a local Memory RAG framework (`~/memory_system`) using [`memory-capture`](memory-capture). This system intercepts requests locally, retrieves policy/vector context, and injects it **before** tokens are transmitted to frontier LLMs.

### System Architecture & Data Flow

```mermaid
flowchart TD
    subgraph LocalMachine["💻 Local Machine (Zero Cloud Tokens Spent)"]
        UserReq["👤 User Request"] --> PrePrompt["⚡ Pre-Prompt Interceptor"]
        PrePrompt --> OKFSearch["📄 OKF File Search<br/>~/memory_system/knowledge/okf"]
        PrePrompt --> ChromaSearch["🔍 ChromaDB Vector Search<br/>~/memory_system/db"]
        OKFSearch --> ContextFormat["📦 Context Formatter"]
        ChromaSearch --> ContextFormat
        ContextFormat --> AugmentedPayload["📝 Augmented Prompt Payload<br/>(System Prompt + RAG + User Query)"]
    end

    subgraph CloudModel["☁️ Frontier LLM Cloud"]
        AugmentedPayload -->|"Encrypted HTTP / Token Stream"| FrontierLLM["🤖 Gemini / Claude / OpenAI"]
        FrontierLLM -->|"Response Stream"| AgentResponse["✨ Synthesized Response"]
    end
```

### Why & How This Functionality Is Organized

- **Deterministic Policy Routing (OKF)**: High-level architectural rules and security standards are stored as plain Markdown under `~/memory_system/knowledge/okf/` for exact, zero-hallucination regex matching.
- **Semantic Memory Indexing (ChromaDB)**: Troubleshooting notes, error logs, and code snippets are embedded locally into ChromaDB at `~/memory_system/db/` using local ONNX embeddings.
- **Automated Inbox Daemon**: Background service `memory-inbox.service` monitors `~/memory_system/inbox/` for new `.md` files and automatically indexes them.
- **Architectural Decision Record**: See [ADR 0005: Local Memory RAG Architecture](docs/adr/0005-local-memory-rag-architecture.md) for rationale.
- **Detailed Documentation**: See the complete [Memory RAG FAQ](memory_rag_faq.md) for step-by-step technical details.

### ⚠️ Gotchas & Operational Caveats

> [!WARNING]
> **Pre-Prompt Token Payload Overflow**: Ingesting raw logs or unchunked files directly into ChromaDB can inflate the injected context payload. Ensure log files are pre-filtered or split into 500–1000 token chunks before dropping into `~/memory_system/inbox/`.

> [!IMPORTANT]
> **Systemd User Daemon Required**: The inbox background watcher relies on `memory-inbox.service` running under `systemctl --user`. If the service is stopped or disabled, files dropped into `inbox/` will sit unprocessed until `python3 ~/memory_system/capture_knowledge.py <file>` is run manually.

> [!CAUTION]
> **OKF vs Chroma Routing Triggers**: Files intended for OKF (deterministic policies) **must** contain `# OKF Decision`, `Type: Policy`, or `Type: Architecture Standard` in their header. Without these exact header strings, `capture_knowledge.py` defaults to embedding the content into ChromaDB vector storage.

> [!NOTE]
> **Directory Tree Initializer**: If `~/memory_system` is missing or cleared, running `python3 ~/memory_system/init_storage.py` must be executed before ingestion to recreate required SQLite tables and collection schemas.

## 📚 Skill Catalog & Navigation

This repository manages **494** modular AI skills across 12 primary domains.

### Overview

| Category | Skills | Quick Link |
|---|---|---|
| [🎨 Design, Film & Video](#-design-film-video) | **28** | [Full Doc ↗](categories/design_film_video.md) |
| [📄 Document & Media Processing](#-document-media-processing) | **8** | [Full Doc ↗](categories/document_media_processing.md) |
| [📓 Notion Integration](#-notion-integration) | **4** | [Full Doc ↗](categories/notion_integration.md) |
| [🤖 AI, RAG & LLM Engineering](#-ai-llm-engineering) | **5** | [Full Doc ↗](categories/ai_llm_engineering.md) |
| [🗄️ Databases & Data Engineering](#-databases-data) | **2** | [Full Doc ↗](categories/databases_data.md) |
| [🔒 Security, Compliance & Hardening](#-security-compliance) | **5** | [Full Doc ↗](categories/security_compliance.md) |
| [☁️ DevOps, Cloud & Infrastructure](#-devops-cloud) | **4** | [Full Doc ↗](categories/devops_cloud.md) |
| [🏗️ Architecture & Engineering Practices](#-software-architecture) | **10** | [Full Doc ↗](categories/software_architecture.md) |
| [💻 Software Engineering & Frameworks](#-software-languages) | **8** | [Full Doc ↗](categories/software_languages.md) |
| [📈 Business, Finance & Strategy](#-business-finance) | **1** | [Full Doc ↗](categories/business_finance.md) |
| [🛠️ Development, Debugging & QA Workflows](#-development-testing) | **25** | [Full Doc ↗](categories/development_testing.md) |
| [💬 Productivity, Research & Communication](#-productivity-comms) | **17** | [Full Doc ↗](categories/productivity_comms.md) |
| [📦 Other User Skills](#-other-user-skills) | **18** | [Full Doc ↗](categories/other_user.md) |

---

### 🎨 Design, Film & Video
📁 *Full Documentation: [🎨 Design, Film & Video Document](categories/design_film_video.md) (28 skills)*

[`algorithmic-art`](algorithmic-art/SKILL.md) • [`artifacts-builder`](artifacts-builder/SKILL.md) • [`brand-guidelines`](brand-guidelines/SKILL.md) • [`canvas-design`](canvas-design/SKILL.md) • [`design-system-starter`](design-system-starter/SKILL.md) • [`director`](director/SKILL.md) • [`draw-io`](draw-io/SKILL.md) • [`excalidraw`](excalidraw/SKILL.md) • [`hyperframes`](hyperframes/SKILL.md) • [`hyperframes-cli`](hyperframes-cli/SKILL.md) • [`hyperframes-registry`](hyperframes-registry/SKILL.md) • [`image-enhancer`](image-enhancer/SKILL.md) • [`marp-slide`](marp-slide/SKILL.md) • [`meme-factory`](meme-factory/SKILL.md) • [`slack-gif-creator`](slack-gif-creator/SKILL.md) • [`startup-business-pipeline`](startup-business-pipeline/SKILL.md) • [`startup-strategy-orchestrator`](startup-strategy-orchestrator/SKILL.md) • [`theme-factory`](theme-factory/SKILL.md) • [`video-brand-pipeline-orchestrator`](video-brand-pipeline-orchestrator/SKILL.md) • [`video-content-orchestrator`](video-content-orchestrator/SKILL.md) • [`video-downloader`](video-downloader/SKILL.md) • [`video-edit`](video-edit/SKILL.md) • [`video-to-landing-page`](video-to-landing-page/SKILL.md) • [`yuv-brand-orchestrator`](yuv-brand-orchestrator/SKILL.md) • [`yuv-decks`](yuv-decks/SKILL.md) • [`yuv-design-system`](yuv-design-system/SKILL.md) • [`yuv-pilot`](yuv-pilot/SKILL.md) • [`yuv-viral-video`](yuv-viral-video/SKILL.md)

### 📄 Document & Media Processing
📁 *Full Documentation: [📄 Document & Media Processing Document](categories/document_media_processing.md) (8 skills)*

[`docx`](docx/SKILL.md) • [`invoice-organizer`](invoice-organizer/SKILL.md) • [`notion-research-documentation`](notion-research-documentation/SKILL.md) • [`pdf`](pdf/SKILL.md) • [`pptx`](pptx/SKILL.md) • [`resemble-detect`](resemble-detect/SKILL.md) • [`web-to-markdown`](web-to-markdown/SKILL.md) • [`xlsx`](xlsx/SKILL.md)

### 📓 Notion Integration
📁 *Full Documentation: [📓 Notion Integration Document](categories/notion_integration.md) (4 skills)*

[`notion-intelligence-orchestrator`](notion-intelligence-orchestrator/SKILL.md) • [`notion-knowledge-capture`](notion-knowledge-capture/SKILL.md) • [`notion-meeting-intelligence`](notion-meeting-intelligence/SKILL.md) • [`notion-spec-to-implementation`](notion-spec-to-implementation/SKILL.md)

### 🤖 AI, RAG & LLM Engineering
📁 *Full Documentation: [🤖 AI, RAG & LLM Engineering Document](categories/ai_llm_engineering.md) (5 skills)*

[`agent-md-refactor`](agent-md-refactor/SKILL.md) • [`gemini`](gemini/SKILL.md) • [`gepetto`](gepetto/SKILL.md) • [`jeffs-automated-build-deploy-agent`](jeffs-automated-build-deploy-agent/SKILL.md) • [`mlops-pipeline-orchestrator`](mlops-pipeline-orchestrator/SKILL.md)

### 🗄️ Databases & Data Engineering
📁 *Full Documentation: [🗄️ Databases & Data Engineering Document](categories/databases_data.md) (2 skills)*

[`data-platform-orchestrator`](data-platform-orchestrator/SKILL.md) • [`database-schema-designer`](database-schema-designer/SKILL.md)

### 🔒 Security, Compliance & Hardening
📁 *Full Documentation: [🔒 Security, Compliance & Hardening Document](categories/security_compliance.md) (5 skills)*

[`anti-reversing-techniques`](anti-reversing-techniques/SKILL.md) • [`dependency-security-audit`](dependency-security-audit/SKILL.md) • [`security-agent-orchestrator`](security-agent-orchestrator/SKILL.md) • [`security-audit-orchestrator`](security-audit-orchestrator/SKILL.md) • [`security-governance-orchestrator`](security-governance-orchestrator/SKILL.md)

### ☁️ DevOps, Cloud & Infrastructure
📁 *Full Documentation: [☁️ DevOps, Cloud & Infrastructure Document](categories/devops_cloud.md) (4 skills)*

[`datadog-cli`](datadog-cli/SKILL.md) • [`github-actions-node24`](github-actions-node24/SKILL.md) • [`incident-diagnostics-pipeline`](incident-diagnostics-pipeline/SKILL.md) • [`trusted-oss-github-setup`](trusted-oss-github-setup/SKILL.md)

### 🏗️ Architecture & Engineering Practices
📁 *Full Documentation: [🏗️ Architecture & Engineering Practices Document](categories/software_architecture.md) (10 skills)*

[`adr-governance-orchestrator`](adr-governance-orchestrator/SKILL.md) • [`architecture-governance-orchestrator`](architecture-governance-orchestrator/SKILL.md) • [`c4-architecture`](c4-architecture/SKILL.md) • [`c4-modeling-pipeline`](c4-modeling-pipeline/SKILL.md) • [`content-governance-orchestrator`](content-governance-orchestrator/SKILL.md) • [`feature-delivery-pipeline`](feature-delivery-pipeline/SKILL.md) • [`frontend-to-backend-requirements`](frontend-to-backend-requirements/SKILL.md) • [`game-changing-features`](game-changing-features/SKILL.md) • [`repo-governance-orchestrator`](repo-governance-orchestrator/SKILL.md) • [`requirements-clarity`](requirements-clarity/SKILL.md)

### 💻 Software Engineering & Frameworks
📁 *Full Documentation: [💻 Software Engineering & Frameworks Document](categories/software_languages.md) (8 skills)*

[`backend-to-frontend-handoff-docs`](backend-to-frontend-handoff-docs/SKILL.md) • [`frontend-design-system-orchestrator`](frontend-design-system-orchestrator/SKILL.md) • [`mui`](mui/SKILL.md) • [`openapi-to-typescript`](openapi-to-typescript/SKILL.md) • [`powershell-pro`](powershell-pro/SKILL.md) • [`react-dev`](react-dev/SKILL.md) • [`react-useeffect`](react-useeffect/SKILL.md) • [`webapp-testing`](webapp-testing/SKILL.md)

### 📈 Business, Finance & Strategy
📁 *Full Documentation: [📈 Business, Finance & Strategy Document](categories/business_finance.md) (1 skills)*

[`seo-content-pipeline`](seo-content-pipeline/SKILL.md)

### 🛠️ Development, Debugging & QA Workflows
📁 *Full Documentation: [🛠️ Development, Debugging & QA Workflows Document](categories/development_testing.md) (25 skills)*

[`adr-authoring`](adr-authoring/SKILL.md) • [`adr-discovery`](adr-discovery/SKILL.md) • [`adr-gatekeeper`](adr-gatekeeper/SKILL.md) • [`adr-lifecycle-management`](adr-lifecycle-management/SKILL.md) • [`changelog-generator`](changelog-generator/SKILL.md) • [`commit-work`](commit-work/SKILL.md) • [`conductor-pipeline-orchestrator`](conductor-pipeline-orchestrator/SKILL.md) • [`context-builder`](context-builder/SKILL.md) • [`custom-code-reviewer`](custom-code-reviewer/SKILL.md) • [`dependency-lifecycle-orchestrator`](dependency-lifecycle-orchestrator/SKILL.md) • [`dependency-release-pipeline`](dependency-release-pipeline/SKILL.md) • [`dependency-updater`](dependency-updater/SKILL.md) • [`elite-code-reviewer`](elite-code-reviewer/SKILL.md) • [`error-diagnostics-orchestrator`](error-diagnostics-orchestrator/SKILL.md) • [`install-adr-gatekeeper`](install-adr-gatekeeper/SKILL.md) • [`mcp-builder`](mcp-builder/SKILL.md) • [`memory-capture`](memory-capture/SKILL.md) • [`performance-optimization-orchestrator`](performance-optimization-orchestrator/SKILL.md) • [`qa-test-planner`](qa-test-planner/SKILL.md) • [`reducing-entropy`](reducing-entropy/SKILL.md) • [`reviewer`](reviewer/SKILL.md) • [`skill-creator`](skill-creator/SKILL.md) • [`skill-judge`](skill-judge/SKILL.md) • [`tdd-pipeline-orchestrator`](tdd-pipeline-orchestrator/SKILL.md) • [`template-skill`](template-skill/SKILL.md)

### 💬 Productivity, Research & Communication
📁 *Full Documentation: [💬 Productivity, Research & Communication Document](categories/productivity_comms.md) (17 skills)*

[`content-research-writer`](content-research-writer/SKILL.md) • [`daily-meeting-update`](daily-meeting-update/SKILL.md) • [`difficult-workplace-conversations`](difficult-workplace-conversations/SKILL.md) • [`domain-name-brainstormer`](domain-name-brainstormer/SKILL.md) • [`feedback-mastery`](feedback-mastery/SKILL.md) • [`file-organizer`](file-organizer/SKILL.md) • [`humanizer`](humanizer/SKILL.md) • [`internal-comms`](internal-comms/SKILL.md) • [`lead-research-assistant`](lead-research-assistant/SKILL.md) • [`lesson-learned`](lesson-learned/SKILL.md) • [`meeting-insights-analyzer`](meeting-insights-analyzer/SKILL.md) • [`naming-analyzer`](naming-analyzer/SKILL.md) • [`professional-communication`](professional-communication/SKILL.md) • [`raffle-winner-picker`](raffle-winner-picker/SKILL.md) • [`researcher`](researcher/SKILL.md) • [`session-handoff`](session-handoff/SKILL.md) • [`writing-clearly-and-concisely`](writing-clearly-and-concisely/SKILL.md)

### 📦 Other User Skills
📁 *Full Documentation: [Other User Skills Document](categories/other_user.md) (18 skills)*

[`advisor`](advisor/SKILL.md) • [`codex`](codex/SKILL.md) • [`command-creator`](command-creator/SKILL.md) • [`competitive-ads-extractor`](competitive-ads-extractor/SKILL.md) • [`crafting-effective-readmes`](crafting-effective-readmes/SKILL.md) • [`delegate`](delegate/SKILL.md) • [`jira`](jira/SKILL.md) • [`mermaid-diagrams`](mermaid-diagrams/SKILL.md) • [`multimedia-production-orchestrator`](multimedia-production-orchestrator/SKILL.md) • [`nano-banana-pro`](nano-banana-pro/SKILL.md) • [`oracle`](oracle/SKILL.md) • [`parallax-landing-page`](parallax-landing-page/SKILL.md) • [`perplexity`](perplexity/SKILL.md) • [`planner`](planner/SKILL.md) • [`plugin-forge`](plugin-forge/SKILL.md) • [`scout`](scout/SKILL.md) • [`ship-learn-next`](ship-learn-next/SKILL.md) • [`worker`](worker/SKILL.md)

