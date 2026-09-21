# My Skills Repository

This repository is a comprehensive collection of AI "skills" designed for various AI harnesses, including Pi-agent, Gemini, and AI coding agent.

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
```

```powershell
# Windows PowerShell
.\setup.ps1 -Client pi
.\setup.ps1 -Client gemini
.\setup.ps1 -Client claude
.\setup.ps1 -Client opencode
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
Inspect host directories, RAG storage presence, and key memory skills:
```bash
./setup.sh --memory                     # Inspect local memory system (OKF + ChromaDB)
```

```powershell
.\setup.ps1 -Memory                     # Windows PowerShell
```

## Deployment

We provide a manifest-driven deployment system to package and deploy skills to different harnesses.

### Deployment Script
The `scripts/deploy_skills.py` script automates the following:
1. **Dependency Resolution**: Recursively identifies all required skills for a given harness.
2. **Package Generation**: Creates a deployment-ready directory (`deploy_package`) containing all necessary skills.
3. **Multi-Harness Support**: Supports `pi`, `gemini`, and `claude` configurations.

### Usage
To plan and generate a deployment package for the `pi` harness:
```bash
python3 scripts/deploy_skills.py --harness pi
```

## Project Structure
- `skills/`: User skills categorized by domain.
- `config-skills/`: System configuration skills.
- `categories/`: Dynamic markdown catalog per category.
- `docs/`: Technical documentation and architecture records.
  - `docs/adr/`: Architecture Decision Records (ADRs) and Governance Strategy.
- `scripts/`:
  - `restore_skills.py`: Core restoration logic for agent clients.
  - `catalog.py`: Skills catalog engine and status inspector.
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

## 🔗 Sequential Pipeline Orchestrators (Grouped Skills)

This repository provides single-call pipeline orchestrators designed to trigger complete, multi-stage workflows across dependent skills. When an agent harness executes one of these grouped skills, each dependent skill is triggered in strict sequential order, passing outputs, reports, and artifacts down the chain.

| Grouped Skill | Workflow Domain | Sequential Dependent Skills Triggered | Output Artifacts Passed Downstream |
|---|---|---|---|
| [`data-platform-orchestrator`](skills/data-platform-orchestrator/SKILL.md) | Data Platform Orchestrator | End-to-end data engineering (Schema $\rightarrow$ dbt $\rightarrow$ Quality $\rightarrow$ Analysis) | Database Schema $\rightarrow$ dbt Models $\rightarrow$ Validation Reports |
| [`security-audit-orchestrator`](skills/security-audit-orchestrator/SKILL.md) | Security Audit Orchestrator | Full security audit lifecycle (Threat Modeling $\rightarrow$ Scanning $\rightarrow$ Forensics $\rightarrow$ Reporting) | Threat Model $\rightarrow$ SAST Reports $\rightarrow$ Forensics $\rightarrow$ Vulnerability Report |
| [`mlops-pipeline-orchestrator`](skills/mlops-pipeline-orchestrator/SKILL.md) | MLOps Pipeline Orchestrator | Production ML lifecycle (Training $\rightarrow$ Deployment $\rightarrow$ Monitoring) | Model Training $\rightarrow$ Deployment Config $\rightarrow$ Monitoring Alerts |
| [`frontend-design-system-orchestrator`](skills/frontend-design-system-orchestrator/SKILL.md) | Frontend Design System Orchestrator | UI/UX and design system consistency (Design $\rightarrow$ Tokens $\rightarrow$ Components $\rightarrow$ Validation) | Design Tokens $\rightarrow$ React Components $\rightarrow$ Visual Validation |
| [`startup-strategy-orchestrator`](skills/startup-strategy-orchestrator/SKILL.md) | Startup Strategy Orchestrator | Startup planning and financial modeling (Market $\rightarrow$ Finance $\rightarrow$ Operations $\rightarrow$ Synthesis) | Market Sizing $\rightarrow$ Financial Model $\rightarrow$ Headcount Plan $\rightarrow$ Business Case |
| [`multimedia-production-orchestrator`](skills/multimedia-production-orchestrator/SKILL.md) | Multimedia Production Orchestrator | Multimedia production (Download $\rightarrow$ Brand $\rightarrow$ Edit $\rightarrow$ Render $\rightarrow$ Landing Page) | Raw Media $\rightarrow$ Brand Tokens $\rightarrow$ Edited Video $\rightarrow$ HyperFrames $\rightarrow$ Landing Page |
| [`tdd-pipeline-orchestrator`](skills/tdd-pipeline-orchestrator/SKILL.md) | TDD Pipeline Orchestrator | Red $\rightarrow$ Green $\rightarrow$ Refactor TDD lifecycle | Failing test suites $\rightarrow$ Passing minimal implementation $\rightarrow$ Refactored clean code |
| [`conductor-pipeline-orchestrator`](skills/conductor-pipeline-orchestrator/SKILL.md) | Conductor Pipeline Orchestrator | Setup $\rightarrow$ Spec & Plan $\rightarrow$ Validation $\rightarrow$ Implementation $\rightarrow$ Status | Tech stack/workflow context $\rightarrow$ `spec.md` & `plan.md` $\rightarrow$ Validation audit $\rightarrow$ Verified task commits $\rightarrow$ Track registry status |
| [`c4-modeling-pipeline`](skills/c4-modeling-pipeline/SKILL.md) | C4 Modeling Pipeline | Bottom-up C4 architecture reverse-engineering (Code $\rightarrow$ Component $\rightarrow$ Container $\rightarrow$ Context $\rightarrow$ ADRs) | Class & entity map $\rightarrow$ Component boundaries $\rightarrow$ Deployment units & APIs $\rightarrow$ System context diagrams $\rightarrow$ Architectural Decision Records |
| [`video-brand-pipeline-orchestrator`](skills/video-brand-pipeline-orchestrator/SKILL.md) | Video Brand Pipeline Orchestrator | Video downloading, brand design tokens, motion editing, viral shorts, and hero landing pages | Raw media & audio stem $\rightarrow$ Brand visual tokens $\rightarrow$ Edited video with kinetic captions $\rightarrow$ Vertical viral MP4 $\rightarrow$ Scroll-driven video hero landing page |
| [`security-agent-orchestrator`](skills/security-agent-orchestrator/SKILL.md) | Security Agent Orchestrator | STRIDE threat modeling, requirements extraction, control mitigation, SAST/deps scanning, hardening, and compliance | STRIDE threat model $\rightarrow$ Security user stories $\rightarrow$ Control mitigation matrix $\rightarrow$ SAST & CVE vulnerability reports $\rightarrow$ Hardened code/configs $\rightarrow$ Compliance certificate & memory sync |
| [`incident-diagnostics-pipeline`](skills/incident-diagnostics-pipeline/SKILL.md) | Incident Diagnostics Pipeline | Telemetry correlation, root-cause analysis, reproduction debugging, fix implementation, and blameless postmortems | Correlated stack traces & telemetry $\rightarrow$ Root Cause Analysis (RCA) $\rightarrow$ Minimal reproduction test case $\rightarrow$ Verified code fix $\rightarrow$ Published blameless postmortem |
| [`feature-delivery-pipeline`](skills/feature-delivery-pipeline/SKILL.md) | Feature Delivery Pipeline | Contract-driven full-stack delivery (Database $\rightarrow$ API contracts $\rightarrow$ Frontend hierarchy $\rightarrow$ Implementation $\rightarrow$ E2E tests) | Database schema & migrations $\rightarrow$ OpenAPI/GraphQL contracts $\rightarrow$ Component tree & API client $\rightarrow$ Integrated full-stack code $\rightarrow$ Passing E2E test report |
| [`seo-content-pipeline`](skills/seo-content-pipeline/SKILL.md) | SEO Content Pipeline | Keyword strategy, article writing, structural/schema optimization, snippet formatting, and E-E-A-T auditing | Article outline & search intent $\rightarrow$ Keyword density & LSI matrix $\rightarrow$ Draft Markdown copy $\rightarrow$ Heading hierarchy & JSON-LD schema $\rightarrow$ Meta titles & snippet blocks $\rightarrow$ E-E-A-T audit scorecard $\rightarrow$ Publication-ready package |
| [`startup-business-pipeline`](skills/startup-business-pipeline/SKILL.md) | Startup Business Pipeline | Market sizing (TAM/SAM/SOM), opportunity analysis, headcount planning, 3-5y financials, competitive analysis, and investor business case | TAM / SAM / SOM calculations $\rightarrow$ Customer ICP & opportunity analysis $\rightarrow$ Phased headcount & compensation model $\rightarrow$ 3-5 year financial forecast & burn rate $\rightarrow$ Competitive differentiation matrix $\rightarrow$ Investor-ready business case |
| [`dependency-release-pipeline`](skills/dependency-release-pipeline/SKILL.md) | Dependency Release Pipeline | Dependency audit, safe upgrade, code review, test verification, enhanced PR creation, and changelog publishing | Dependency vulnerability & outdated report $\rightarrow$ Updated lockfiles & migrated syntax $\rightarrow$ Code review assessment $\rightarrow$ Verified test suite pass $\rightarrow$ Enhanced Pull Request with checklists $\rightarrow$ Published `CHANGELOG.md` entry |
