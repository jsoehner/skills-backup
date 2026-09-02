# ⚡ OpenCode & Multi-Harness AI Skills Repository

A centralized, enterprise-grade repository of modular AI agent skills supporting **OpenCode**, **Gemini CLI**, **Claude Code**, and **Pi-Agent** harnesses. Each skill provides self-contained domain expertise, deterministic policies, step-by-step procedures, and execution playbooks.

> [!NOTE]
> **Tier 1 Architecture Standardization**: As of `v1.2.0`, the repository structure has been migrated to standardize all skills under the `skills/` namespace (see [ADR 0006](docs/adr/0006-standardize-skills-directory-structure.md)).

---

## 🏗️ Architecture & Taxonomy

We employ a dual-layered, modular architecture to distinguish fundamental capabilities from orchestrations:

```mermaid
graph TD
    subgraph Repo["📁 Repository Root (skills-backup/)"]
        Skills["📂 skills/<br/>(Atomic & Custom User Skills)"]
        ConfigSkills["📂 skills/config-skills/<br/>(System Configuration Skills)"]
        Composites["📦 Root Composite Skills<br/>(manifest.json + SKILL.md)"]
    end

    subgraph SyncTooling["⚡ Synchronization & Deployment Pipeline"]
        SyncPy["sync.py<br/>(Bi-directional Deploy & Save)"]
        RestorePy["restore_skills.py<br/>(Clean Client Restore)"]
        DeployPy["deploy_skills.py<br/>(Multi-Harness Packaging)"]
        UpdateReadme["update_readme.py<br/>(Dynamic Index & Memory RAG)"]
    end

    subgraph TargetRuntimes["💻 AI Harness Runtime Locations"]
        OpenCode["~/.opencode/skills/"]
        Gemini["~/.gemini/config/skills/"]
        Claude["~/.claude/skills/"]
        Pi["~/.pi/agent/skills/"]
    end

    Repo --> SyncTooling
    SyncTooling --> TargetRuntimes
```

### 1. Atomic Skills (`skills/`)
Self-contained, modular building blocks providing specialized capabilities across software engineering, security, databases, DevOps, and media processing. Atomic skills have no internal dependencies on other skills.

### 2. System Configuration Skills (`skills/config-skills/`)
Pre-configured baseline skills provisioned for AI assistant runtimes (such as cloud database connectors, framework analyzers, and security scanners).

### 3. Composite Skills (Root / Orchestrators)
High-level workflows and multi-agent orchestrations that depend on one or more Atomic skills. Composite skills require:
- A `manifest.json` describing metadata, type (`composite`), and required `dependencies`.
- A `SKILL.md` documenting workflow orchestration, preconditions, and pitfalls.

---

## 🛠️ Usage & Management Workflows

### 1. Bi-directional Synchronization (`sync.py`)
Deploy skills from the repo into your active AI client directory, or capture local modifications made during agent sessions back to the repository:

```bash
# Deploy skills from repo to active AI client runtime (default: pi)
python3 sync.py deploy --client gemini

# Save local agent modifications from client runtime back into repo
python3 sync.py save --client gemini

# Selective category synchronization
python3 sync.py deploy --client opencode -g databases_data

# List all available custom and system configuration skill categories
python3 sync.py -l
```

### 2. Clean Environment Restoration (`restore_skills.py`)
Installs and flattens unique skills directly into client config directories, automatically stripping nested subdirectories:

```bash
# Restore to OpenCode (~/.opencode/skills)
python3 restore_skills.py . --client opencode

# Restore to Gemini (~/.gemini/config/skills)
python3 restore_skills.py . --client gemini

# Restore to Claude Code (~/.claude/skills)
python3 restore_skills.py . --client claude

# Restore to Pi Agent (~/.pi/agent/skills)
python3 restore_skills.py . --client pi
```

### 3. Multi-Harness Packaging & Dependency Resolution (`deploy_skills.py`)
Recursively resolves the dependency graph for composite skills and creates deployable packages:

```bash
# Dry-run plan for Pi harness
python3 deploy_skills.py --dry-run --harness pi

# Generate deployment package for Claude
python3 deploy_skills.py --harness claude
```

### 4. Dynamic Catalog & Documentation Generator (`update_readme.py`)
Scans frontmatter across `skills/` and `skills/config-skills/`, generates domain markdown indexes in `categories/`, and rebuilds this README:

```bash
python3 update_readme.py
```

---

## 🔍 Verification Methods & Diagnostic Testing

To verify the integrity, synchronization, and catalog indexing across the repository:

### Test Suite 1: Dynamic Catalog Index Verification
Run `update_readme.py` to verify that all user and configuration skills are discovered and cataloged without frontmatter syntax errors:

```bash
python3 update_readme.py
```
**Verified Output**:
```text
README.md and category documents updated successfully with 463 user skills and 363 config skills.
```

### Test Suite 2: Category Taxonomy & Grouping Verification
Validate that all 12 custom user domains and 7 system configuration domains resolve correctly:

```bash
python3 sync.py -l
```
**Verified Output**:
```text
Available Custom User Skill Groups:
  - design_film_video              (🎨 Design, Film & Video)
  - document_media_processing      (📄 Document & Media Processing)
  - notion_integration             (📓 Notion Integration)
  - ai_llm_engineering             (🤖 AI, RAG & LLM Engineering)
  - databases_data                 (🗄️ Databases & Data Engineering)
  - security_compliance            (🔒 Security, Compliance & Hardening)
  - devops_cloud                   (☁️ DevOps, Cloud & Infrastructure)
  - software_architecture          (🏗️ Architecture & Engineering Practices)
  - software_languages             (💻 Software Engineering & Frameworks)
  - business_finance               (📈 Business, Finance & Strategy)
  - development_testing            (🛠️ Development, Debugging & QA Workflows)
  - productivity_comms             (💬 Productivity, Research & Communication)

Available System Config Skill Groups:
  - databases_data                 (🗄️ Databases & Data Engineering)
  - security_compliance            (🔒 Security, Compliance & Hardening)
  - devops_infra                   (☁️ DevOps & Infrastructure)
  - agent_orchestration            (🤖 Agent Orchestration & Workflow)
  - software_languages             (💻 Software Engineering (Languages & APIs))
  - business_finance               (📈 Business & Financial Analysis)
  - other                          (Uncategorized)
```

### Test Suite 3: Dependency Resolution & Packaging Test
Execute a dry-run deployment to verify recursive DAG dependency resolution for composite skills:

```bash
python3 deploy_skills.py --dry-run --harness pi
```
**Verified Output**:
```text
Scanning directory: /home/jsoehner/skills-backup
Scanning skills path: /home/jsoehner/skills-backup/skills
--- Planning Deployment for Harness: pi ---
Total skills to include (262):
 - accessibility-compliance-accessibility-audit
 - accidental-data-loss-prevention
 - adr-authoring
 - adr-discovery
 - adr-lifecycle-management
 ... [257 additional skills resolved]
```

### Test Suite 4: Tree Integrity & Manifest Diagnostic Scan
Verify the presence of `SKILL.md` definitions and manifest configurations:

```bash
python3 debug_scan.py
```
**Verified Output**:
```text
Skills path: ./skills
Skills path exists.
Found SKILL.md in: ./skills/accessibility-compliance-accessibility-audit
Skill name: accessibility-compliance-accessibility-audit
...
```

### Test Suite 5: Audit Status Integrity
Verify that `audit_status.json` maintains valid JSON mapping with 0 orphaned paths:

```bash
python3 -c "import json; data=json.load(open('audit_status.json')); print(f'Valid JSON with {len(data)} entries')"
```
**Verified Output**:
```text
Valid JSON with 599 entries
```

---

## 📁 Project Structure

```text
skills-backup/
├── skills/                     # All Atomic and Modular Skills
│   ├── config-skills/          # System configuration & connector skills
│   └── [skill-name]/           # Individual skill directory (contains SKILL.md)
├── docs/                       # Architectural governance & documentation
│   ├── adr/                    # Architecture Decision Records (ADRs)
│   ├── adr-templates/          # Official ADR markdown templates
│   └── decisions/              # Decision strategies & policies
├── categories/                 # Auto-generated category index documentation
├── audit_status.json           # Categorization and migration source of truth
├── sync.py                     # Bi-directional local sync engine
├── restore_skills.py           # Client environment restoration utility
├── deploy_skills.py            # Multi-harness packaging & dependency resolver
├── update_readme.py            # Dynamic catalog & documentation generator
├── debug_scan.py               # Integrity & diagnostics scanner
├── AGENTS.md                   # Agent system prompt configuration
├── CONTRIBUTING.md             # Contributor workflows & standards
├── LIFECYCLE.md                # Lifecycle & operations guide
├── CHANGELOG.md                # Version history & migration notes
└── README.md                   # Primary project documentation
```

---

## 🤝 Contributing & ADR Governance

1. **Atomic Skills**: Add new modular skills directly to `skills/<skill-name>/SKILL.md`.
2. **Composite Skills**: Add orchestrators with a `manifest.json` declaring dependencies.
3. **Architectural Changes**: All structural or breaking changes require an Architectural Decision Record in `docs/adr/` following the [ADR Governance Strategy](docs/decisions/ADR_Governance_Strategy.md).


## 🧠 Local Memory RAG Architecture & Token Flow

The repository integrates a local Memory RAG framework (`~/memory_system`) using [`memory-capture`](skills/memory-capture). This system intercepts requests locally, retrieves policy/vector context, and injects it **before** tokens are transmitted to frontier LLMs.

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

This repository manages **826** modular AI skills across 12 primary domains.

### Overview

| Category | Skills | Quick Link |
|---|---|---|
| [🎨 Design, Film & Video](#-design-film-video) | **36** | [Full Doc ↗](categories/design_film_video.md) |
| [📄 Document & Media Processing](#-document-media-processing) | **11** | [Full Doc ↗](categories/document_media_processing.md) |
| [📓 Notion Integration](#-notion-integration) | **4** | [Full Doc ↗](categories/notion_integration.md) |
| [🤖 AI, RAG & LLM Engineering](#-ai-llm-engineering) | **29** | [Full Doc ↗](categories/ai_llm_engineering.md) |
| [🗄️ Databases & Data Engineering](#-databases-data) | **71** | [Full Doc ↗](categories/databases_data.md) |
| [🔒 Security, Compliance & Hardening](#-security-compliance) | **34** | [Full Doc ↗](categories/security_compliance.md) |
| [☁️ DevOps, Cloud & Infrastructure](#-devops-cloud) | **43** | [Full Doc ↗](categories/devops_cloud.md) |
| [🏗️ Architecture & Engineering Practices](#-software-architecture) | **31** | [Full Doc ↗](categories/software_architecture.md) |
| [💻 Software Engineering & Frameworks](#-software-languages) | **65** | [Full Doc ↗](categories/software_languages.md) |
| [📈 Business, Finance & Strategy](#-business-finance) | **22** | [Full Doc ↗](categories/business_finance.md) |
| [🛠️ Development, Debugging & QA Workflows](#-development-testing) | **67** | [Full Doc ↗](categories/development_testing.md) |
| [💬 Productivity, Research & Communication](#-productivity-comms) | **18** | [Full Doc ↗](categories/productivity_comms.md) |
| [📦 Other User Skills](#-other-user-skills) | **32** | [Full Doc ↗](categories/other_user.md) |

---

### 🎨 Design, Film & Video
📁 *Full Documentation: [🎨 Design, Film & Video Document](categories/design_film_video.md) (36 skills)*

[`algorithmic-art`](skills/algorithmic-art/SKILL.md) • [`article-illustrations`](skills/article-illustrations/SKILL.md) • [`artifacts-builder`](skills/artifacts-builder/SKILL.md) • [`brand-guidelines`](skills/brand-guidelines/SKILL.md) • [`canvas-design`](skills/canvas-design/SKILL.md) • [`debugging-toolkit-smart-debug`](skills/debugging-toolkit-smart-debug/SKILL.md) • [`design-system-starter`](skills/design-system-starter/SKILL.md) • [`director`](skills/director/SKILL.md) • [`draw-io`](skills/draw-io/SKILL.md) • [`error-diagnostics-smart-debug`](skills/error-diagnostics-smart-debug/SKILL.md) • [`excalidraw`](skills/excalidraw/SKILL.md) • [`helm-chart-scaffolding`](skills/helm-chart-scaffolding/SKILL.md) • [`hyperframes`](skills/hyperframes/SKILL.md) • [`hyperframes-cli`](skills/hyperframes-cli/SKILL.md) • [`hyperframes-registry`](skills/hyperframes-registry/SKILL.md) • [`image-enhancer`](skills/image-enhancer/SKILL.md) • [`incident-response-smart-fix`](skills/incident-response-smart-fix/SKILL.md) • [`marp-slide`](skills/marp-slide/SKILL.md) • [`meme-factory`](skills/meme-factory/SKILL.md) • [`slack-gif-creator`](skills/slack-gif-creator/SKILL.md) • [`startup-analyst`](skills/startup-analyst/SKILL.md) • [`startup-business-analyst-business-case`](skills/startup-business-analyst-business-case/SKILL.md) • [`startup-business-analyst-financial-projections`](skills/startup-business-analyst-financial-projections/SKILL.md) • [`startup-business-analyst-market-opportunity`](skills/startup-business-analyst-market-opportunity/SKILL.md) • [`startup-financial-modeling`](skills/startup-financial-modeling/SKILL.md) • [`startup-metrics-framework`](skills/startup-metrics-framework/SKILL.md) • [`theme-factory`](skills/theme-factory/SKILL.md) • [`video-content-orchestrator`](skills/video-content-orchestrator/SKILL.md) • [`video-downloader`](skills/video-downloader/SKILL.md) • [`video-edit`](skills/video-edit/SKILL.md) • [`video-to-landing-page`](skills/video-to-landing-page/SKILL.md) • [`yuv-brand-orchestrator`](skills/yuv-brand-orchestrator/SKILL.md) • [`yuv-decks`](skills/yuv-decks/SKILL.md) • [`yuv-design-system`](skills/yuv-design-system/SKILL.md) • [`yuv-pilot`](skills/yuv-pilot/SKILL.md) • [`yuv-viral-video`](skills/yuv-viral-video/SKILL.md)

### 📄 Document & Media Processing
📁 *Full Documentation: [📄 Document & Media Processing Document](categories/document_media_processing.md) (11 skills)*

[`api-documenter`](skills/api-documenter/SKILL.md) • [`code-documentation-code-explain`](skills/code-documentation-code-explain/SKILL.md) • [`code-documentation-doc-generate`](skills/code-documentation-doc-generate/SKILL.md) • [`documentation-generation-doc-generate`](skills/documentation-generation-doc-generate/SKILL.md) • [`invoice-organizer`](skills/invoice-organizer/SKILL.md) • [`notion-research-documentation`](skills/notion-research-documentation/SKILL.md) • [`pdf`](skills/pdf/SKILL.md) • [`pptx`](skills/pptx/SKILL.md) • [`resemble-detect`](skills/resemble-detect/SKILL.md) • [`web-to-markdown`](skills/web-to-markdown/SKILL.md) • [`xlsx`](skills/xlsx/SKILL.md)

### 📓 Notion Integration
📁 *Full Documentation: [📓 Notion Integration Document](categories/notion_integration.md) (4 skills)*

[`notion-intelligence-orchestrator`](skills/notion-intelligence-orchestrator/SKILL.md) • [`notion-knowledge-capture`](skills/notion-knowledge-capture/SKILL.md) • [`notion-meeting-intelligence`](skills/notion-meeting-intelligence/SKILL.md) • [`notion-spec-to-implementation`](skills/notion-spec-to-implementation/SKILL.md)

### 🤖 AI, RAG & LLM Engineering
📁 *Full Documentation: [🤖 AI, RAG & LLM Engineering Document](categories/ai_llm_engineering.md) (29 skills)*

[`agent-md-refactor`](skills/agent-md-refactor/SKILL.md) • [`agent-orchestration-improve-agent`](skills/agent-orchestration-improve-agent/SKILL.md) • [`agent-orchestration-multi-agent-optimize`](skills/agent-orchestration-multi-agent-optimize/SKILL.md) • [`ai-engineer`](skills/ai-engineer/SKILL.md) • [`cloud-sql-postgres-vectorassist`](skills/cloud-sql-postgres-vectorassist/SKILL.md) • [`code-review-ai-ai-review`](skills/code-review-ai-ai-review/SKILL.md) • [`embedding-strategies`](skills/embedding-strategies/SKILL.md) • [`error-debugging-multi-agent-review`](skills/error-debugging-multi-agent-review/SKILL.md) • [`gemini`](skills/gemini/SKILL.md) • [`gepetto`](skills/gepetto/SKILL.md) • [`hybrid-search-implementation`](skills/hybrid-search-implementation/SKILL.md) • [`langchain-architecture`](skills/langchain-architecture/SKILL.md) • [`llm-application-dev-ai-assistant`](skills/llm-application-dev-ai-assistant/SKILL.md) • [`llm-application-dev-langchain-agent`](skills/llm-application-dev-langchain-agent/SKILL.md) • [`llm-application-dev-prompt-optimize`](skills/llm-application-dev-prompt-optimize/SKILL.md) • [`llm-evaluation`](skills/llm-evaluation/SKILL.md) • [`machine-learning-ops-ml-pipeline`](skills/machine-learning-ops-ml-pipeline/SKILL.md) • [`ml-best-practices`](skills/ml-best-practices/SKILL.md) • [`ml-engineer`](skills/ml-engineer/SKILL.md) • [`ml-pipeline-workflow`](skills/ml-pipeline-workflow/SKILL.md) • [`mlops-engineer`](skills/mlops-engineer/SKILL.md) • [`performance-testing-review-ai-review`](skills/performance-testing-review-ai-review/SKILL.md) • [`performance-testing-review-multi-agent-review`](skills/performance-testing-review-multi-agent-review/SKILL.md) • [`prompt-engineer`](skills/prompt-engineer/SKILL.md) • [`prompt-engineering-patterns`](skills/prompt-engineering-patterns/SKILL.md) • [`rag-implementation`](skills/rag-implementation/SKILL.md) • [`similarity-search-patterns`](skills/similarity-search-patterns/SKILL.md) • [`vector-database-engineer`](skills/vector-database-engineer/SKILL.md) • [`vector-index-tuning`](skills/vector-index-tuning/SKILL.md)

### 🗄️ Databases & Data Engineering
📁 *Full Documentation: [🗄️ Databases & Data Engineering Document](categories/databases_data.md) (71 skills)*

[`accidental-data-loss-prevention`](skills/accidental-data-loss-prevention/SKILL.md) • [`airflow-dag-patterns`](skills/airflow-dag-patterns/SKILL.md) • [`alloydb-omni-access-control`](skills/alloydb-omni-access-control/SKILL.md) • [`alloydb-omni-container`](skills/alloydb-omni-container/SKILL.md) • [`alloydb-omni-data`](skills/alloydb-omni-data/SKILL.md) • [`alloydb-omni-health`](skills/alloydb-omni-health/SKILL.md) • [`alloydb-omni-kubernetes`](skills/alloydb-omni-kubernetes/SKILL.md) • [`alloydb-omni-monitor`](skills/alloydb-omni-monitor/SKILL.md) • [`alloydb-omni-optimize`](skills/alloydb-omni-optimize/SKILL.md) • [`alloydb-omni-performance`](skills/alloydb-omni-performance/SKILL.md) • [`alloydb-omni-replication`](skills/alloydb-omni-replication/SKILL.md) • [`alloydb-postgres-access-management`](skills/alloydb-postgres-access-management/SKILL.md) • [`alloydb-postgres-admin`](skills/alloydb-postgres-admin/SKILL.md) • [`alloydb-postgres-data`](skills/alloydb-postgres-data/SKILL.md) • [`alloydb-postgres-health`](skills/alloydb-postgres-health/SKILL.md) • [`alloydb-postgres-monitor`](skills/alloydb-postgres-monitor/SKILL.md) • [`alloydb-postgres-optimize`](skills/alloydb-postgres-optimize/SKILL.md) • [`alloydb-postgres-replication`](skills/alloydb-postgres-replication/SKILL.md) • [`angular-migration`](skills/angular-migration/SKILL.md) • [`bigquery`](skills/bigquery/SKILL.md) • [`bigquery-data-transfer-service`](skills/bigquery-data-transfer-service/SKILL.md) • [`building-data-apps`](skills/building-data-apps/SKILL.md) • [`cloud-sql-mysql-admin`](skills/cloud-sql-mysql-admin/SKILL.md) • [`cloud-sql-mysql-data`](skills/cloud-sql-mysql-data/SKILL.md) • [`cloud-sql-mysql-lifecycle`](skills/cloud-sql-mysql-lifecycle/SKILL.md) • [`cloud-sql-mysql-monitor`](skills/cloud-sql-mysql-monitor/SKILL.md) • [`cloud-sql-postgres-admin`](skills/cloud-sql-postgres-admin/SKILL.md) • [`cloud-sql-postgres-data`](skills/cloud-sql-postgres-data/SKILL.md) • [`cloud-sql-postgres-health`](skills/cloud-sql-postgres-health/SKILL.md) • [`cloud-sql-postgres-lifecycle`](skills/cloud-sql-postgres-lifecycle/SKILL.md) • [`cloud-sql-postgres-monitor`](skills/cloud-sql-postgres-monitor/SKILL.md) • [`cloud-sql-postgres-replication`](skills/cloud-sql-postgres-replication/SKILL.md) • [`cloud-sql-postgres-view-config`](skills/cloud-sql-postgres-view-config/SKILL.md) • [`cloud-sql-sqlserver-admin`](skills/cloud-sql-sqlserver-admin/SKILL.md) • [`cloud-sql-sqlserver-data`](skills/cloud-sql-sqlserver-data/SKILL.md) • [`cloud-sql-sqlserver-lifecycle`](skills/cloud-sql-sqlserver-lifecycle/SKILL.md) • [`cloud-sql-sqlserver-monitor`](skills/cloud-sql-sqlserver-monitor/SKILL.md) • [`data-autocleaning`](skills/data-autocleaning/SKILL.md) • [`data-engineer`](skills/data-engineer/SKILL.md) • [`data-engineering-data-driven-feature`](skills/data-engineering-data-driven-feature/SKILL.md) • [`data-engineering-data-pipeline`](skills/data-engineering-data-pipeline/SKILL.md) • [`data-quality-frameworks`](skills/data-quality-frameworks/SKILL.md) • [`data-scientist`](skills/data-scientist/SKILL.md) • [`data-storytelling`](skills/data-storytelling/SKILL.md) • [`database-admin`](skills/database-admin/SKILL.md) • [`database-architect`](skills/database-architect/SKILL.md) • [`database-cloud-optimization-cost-optimize`](skills/database-cloud-optimization-cost-optimize/SKILL.md) • [`database-migration`](skills/database-migration/SKILL.md) • [`database-migrations-migration-observability`](skills/database-migrations-migration-observability/SKILL.md) • [`database-migrations-sql-migrations`](skills/database-migrations-sql-migrations/SKILL.md) • [`database-optimizer`](skills/database-optimizer/SKILL.md) • [`database-schema-designer`](skills/database-schema-designer/SKILL.md) • [`dataform-bigquery`](skills/dataform-bigquery/SKILL.md) • [`dbt-bigquery`](skills/dbt-bigquery/SKILL.md) • [`dbt-transformation-patterns`](skills/dbt-transformation-patterns/SKILL.md) • [`discovering-gcp-data-assets`](skills/discovering-gcp-data-assets/SKILL.md) • [`federate-lakehouse-catalog`](skills/federate-lakehouse-catalog/SKILL.md) • [`firestore-data`](skills/firestore-data/SKILL.md) • [`framework-migration-code-migrate`](skills/framework-migration-code-migrate/SKILL.md) • [`framework-migration-deps-upgrade`](skills/framework-migration-deps-upgrade/SKILL.md) • [`framework-migration-legacy-modernize`](skills/framework-migration-legacy-modernize/SKILL.md) • [`gcp-data-pipelines`](skills/gcp-data-pipelines/SKILL.md) • [`gcp-managed-airflow-migrations`](skills/gcp-managed-airflow-migrations/SKILL.md) • [`gcp-spark`](skills/gcp-spark/SKILL.md) • [`gcs-security-assessment`](skills/gcs-security-assessment/SKILL.md) • [`gdpr-data-handling`](skills/gdpr-data-handling/SKILL.md) • [`postgresql`](skills/postgresql/SKILL.md) • [`spanner-data`](skills/spanner-data/SKILL.md) • [`spark-optimization`](skills/spark-optimization/SKILL.md) • [`sql-optimization-patterns`](skills/sql-optimization-patterns/SKILL.md) • [`sql-pro`](skills/sql-pro/SKILL.md)

### 🔒 Security, Compliance & Hardening
📁 *Full Documentation: [🔒 Security, Compliance & Hardening Document](categories/security_compliance.md) (34 skills)*

[`accessibility-compliance-accessibility-audit`](skills/accessibility-compliance-accessibility-audit/SKILL.md) • [`adr-authoring`](skills/adr-authoring/SKILL.md) • [`anti-reversing-techniques`](skills/anti-reversing-techniques/SKILL.md) • [`attack-tree-construction`](skills/attack-tree-construction/SKILL.md) • [`auth-implementation-patterns`](skills/auth-implementation-patterns/SKILL.md) • [`backend-security-coder`](skills/backend-security-coder/SKILL.md) • [`binary-analysis-patterns`](skills/binary-analysis-patterns/SKILL.md) • [`codebase-cleanup-deps-audit`](skills/codebase-cleanup-deps-audit/SKILL.md) • [`dependency-management-deps-audit`](skills/dependency-management-deps-audit/SKILL.md) • [`frontend-mobile-security-xss-scan`](skills/frontend-mobile-security-xss-scan/SKILL.md) • [`frontend-security-coder`](skills/frontend-security-coder/SKILL.md) • [`gcloud-auth-verification`](skills/gcloud-auth-verification/SKILL.md) • [`k8s-security-policies`](skills/k8s-security-policies/SKILL.md) • [`malware-analyst`](skills/malware-analyst/SKILL.md) • [`mobile-security-coder`](skills/mobile-security-coder/SKILL.md) • [`mtls-configuration`](skills/mtls-configuration/SKILL.md) • [`pci-compliance`](skills/pci-compliance/SKILL.md) • [`sast-configuration`](skills/sast-configuration/SKILL.md) • [`secrets-management`](skills/secrets-management/SKILL.md) • [`security-auditor`](skills/security-auditor/SKILL.md) • [`security-compliance-compliance-check`](skills/security-compliance-compliance-check/SKILL.md) • [`security-governance-orchestrator`](skills/security-governance-orchestrator/SKILL.md) • [`security-requirement-extraction`](skills/security-requirement-extraction/SKILL.md) • [`security-scanning-security-dependencies`](skills/security-scanning-security-dependencies/SKILL.md) • [`security-scanning-security-hardening`](skills/security-scanning-security-hardening/SKILL.md) • [`security-scanning-security-sast`](skills/security-scanning-security-sast/SKILL.md) • [`security-tech-debt`](skills/security-tech-debt/SKILL.md) • [`seo-authority-builder`](skills/seo-authority-builder/SKILL.md) • [`seo-content-auditor`](skills/seo-content-auditor/SKILL.md) • [`solidity-security`](skills/solidity-security/SKILL.md) • [`stride-analysis-patterns`](skills/stride-analysis-patterns/SKILL.md) • [`threat-mitigation-mapping`](skills/threat-mitigation-mapping/SKILL.md) • [`threat-modeling-expert`](skills/threat-modeling-expert/SKILL.md) • [`wcag-audit-patterns`](skills/wcag-audit-patterns/SKILL.md)

### ☁️ DevOps, Cloud & Infrastructure
📁 *Full Documentation: [☁️ DevOps, Cloud & Infrastructure Document](categories/devops_cloud.md) (43 skills)*

[`api-testing-observability-api-mock`](skills/api-testing-observability-api-mock/SKILL.md) • [`bazel-build-optimization`](skills/bazel-build-optimization/SKILL.md) • [`c4-container`](skills/c4-container/SKILL.md) • [`cost-optimization`](skills/cost-optimization/SKILL.md) • [`datadog-cli`](skills/datadog-cli/SKILL.md) • [`deployment-engineer`](skills/deployment-engineer/SKILL.md) • [`deployment-pipeline-design`](skills/deployment-pipeline-design/SKILL.md) • [`deployment-validation-config-validate`](skills/deployment-validation-config-validate/SKILL.md) • [`devops-troubleshooter`](skills/devops-troubleshooter/SKILL.md) • [`distributed-tracing`](skills/distributed-tracing/SKILL.md) • [`gcp-composer-troubleshooting`](skills/gcp-composer-troubleshooting/SKILL.md) • [`gcp-dataflow`](skills/gcp-dataflow/SKILL.md) • [`gcp-pipeline-orchestration`](skills/gcp-pipeline-orchestration/SKILL.md) • [`gcp-pipeline-resource-provisioning`](skills/gcp-pipeline-resource-provisioning/SKILL.md) • [`github-actions-node24`](skills/github-actions-node24/SKILL.md) • [`github-actions-templates`](skills/github-actions-templates/SKILL.md) • [`gitlab-ci-patterns`](skills/gitlab-ci-patterns/SKILL.md) • [`gitops-workflow`](skills/gitops-workflow/SKILL.md) • [`grafana-dashboards`](skills/grafana-dashboards/SKILL.md) • [`hybrid-cloud-networking`](skills/hybrid-cloud-networking/SKILL.md) • [`incident-responder`](skills/incident-responder/SKILL.md) • [`incident-response-incident-response`](skills/incident-response-incident-response/SKILL.md) • [`incident-runbook-templates`](skills/incident-runbook-templates/SKILL.md) • [`istio-traffic-management`](skills/istio-traffic-management/SKILL.md) • [`k8s-manifest-generator`](skills/k8s-manifest-generator/SKILL.md) • [`kubernetes-architect`](skills/kubernetes-architect/SKILL.md) • [`linkerd-patterns`](skills/linkerd-patterns/SKILL.md) • [`monorepo-architect`](skills/monorepo-architect/SKILL.md) • [`monorepo-management`](skills/monorepo-management/SKILL.md) • [`network-engineer`](skills/network-engineer/SKILL.md) • [`nx-workspace-patterns`](skills/nx-workspace-patterns/SKILL.md) • [`observability-engineer`](skills/observability-engineer/SKILL.md) • [`observability-monitoring-monitor-setup`](skills/observability-monitoring-monitor-setup/SKILL.md) • [`observability-monitoring-slo-implement`](skills/observability-monitoring-slo-implement/SKILL.md) • [`on-call-handoff-patterns`](skills/on-call-handoff-patterns/SKILL.md) • [`postmortem-writing`](skills/postmortem-writing/SKILL.md) • [`prometheus-configuration`](skills/prometheus-configuration/SKILL.md) • [`service-mesh-expert`](skills/service-mesh-expert/SKILL.md) • [`service-mesh-observability`](skills/service-mesh-observability/SKILL.md) • [`slo-implementation`](skills/slo-implementation/SKILL.md) • [`terraform-module-library`](skills/terraform-module-library/SKILL.md) • [`terraform-specialist`](skills/terraform-specialist/SKILL.md) • [`turborepo-caching`](skills/turborepo-caching/SKILL.md)

### 🏗️ Architecture & Engineering Practices
📁 *Full Documentation: [🏗️ Architecture & Engineering Practices Document](categories/software_architecture.md) (31 skills)*

[`architect-review`](skills/architect-review/SKILL.md) • [`architecture-decision-records`](skills/architecture-decision-records/SKILL.md) • [`architecture-governance-orchestrator`](skills/architecture-governance-orchestrator/SKILL.md) • [`architecture-patterns`](skills/architecture-patterns/SKILL.md) • [`backend-architect`](skills/backend-architect/SKILL.md) • [`backend-development-feature-development`](skills/backend-development-feature-development/SKILL.md) • [`c4-architecture`](skills/c4-architecture/SKILL.md) • [`c4-architecture-c4-architecture`](skills/c4-architecture-c4-architecture/SKILL.md) • [`c4-code`](skills/c4-code/SKILL.md) • [`c4-component`](skills/c4-component/SKILL.md) • [`c4-context`](skills/c4-context/SKILL.md) • [`cloud-architect`](skills/cloud-architect/SKILL.md) • [`content-governance-orchestrator`](skills/content-governance-orchestrator/SKILL.md) • [`cqrs-implementation`](skills/cqrs-implementation/SKILL.md) • [`docs-architect`](skills/docs-architect/SKILL.md) • [`dotnet-architect`](skills/dotnet-architect/SKILL.md) • [`event-sourcing-architect`](skills/event-sourcing-architect/SKILL.md) • [`event-store-design`](skills/event-store-design/SKILL.md) • [`frontend-to-backend-requirements`](skills/frontend-to-backend-requirements/SKILL.md) • [`full-stack-orchestration-full-stack-feature`](skills/full-stack-orchestration-full-stack-feature/SKILL.md) • [`game-changing-features`](skills/game-changing-features/SKILL.md) • [`git-pr-workflows-onboard`](skills/git-pr-workflows-onboard/SKILL.md) • [`graphql-architect`](skills/graphql-architect/SKILL.md) • [`hybrid-cloud-architect`](skills/hybrid-cloud-architect/SKILL.md) • [`microservices-patterns`](skills/microservices-patterns/SKILL.md) • [`multi-cloud-architecture`](skills/multi-cloud-architecture/SKILL.md) • [`react-native-architecture`](skills/react-native-architecture/SKILL.md) • [`requirements-clarity`](skills/requirements-clarity/SKILL.md) • [`saga-orchestration`](skills/saga-orchestration/SKILL.md) • [`seo-structure-architect`](skills/seo-structure-architect/SKILL.md) • [`systems-programming-rust-project`](skills/systems-programming-rust-project/SKILL.md)

### 💻 Software Engineering & Frameworks
📁 *Full Documentation: [💻 Software Engineering & Frameworks Document](categories/software_languages.md) (65 skills)*

[`api-design-principles`](skills/api-design-principles/SKILL.md) • [`arm-cortex-expert`](skills/arm-cortex-expert/SKILL.md) • [`async-python-patterns`](skills/async-python-patterns/SKILL.md) • [`backend-to-frontend-handoff-docs`](skills/backend-to-frontend-handoff-docs/SKILL.md) • [`bash-defensive-patterns`](skills/bash-defensive-patterns/SKILL.md) • [`bash-pro`](skills/bash-pro/SKILL.md) • [`bats-testing-patterns`](skills/bats-testing-patterns/SKILL.md) • [`blockchain-developer`](skills/blockchain-developer/SKILL.md) • [`c-pro`](skills/c-pro/SKILL.md) • [`cpp-pro`](skills/cpp-pro/SKILL.md) • [`csharp-pro`](skills/csharp-pro/SKILL.md) • [`defi-protocol-templates`](skills/defi-protocol-templates/SKILL.md) • [`django-pro`](skills/django-pro/SKILL.md) • [`dotnet-backend-patterns`](skills/dotnet-backend-patterns/SKILL.md) • [`elixir-pro`](skills/elixir-pro/SKILL.md) • [`fastapi-pro`](skills/fastapi-pro/SKILL.md) • [`fastapi-templates`](skills/fastapi-templates/SKILL.md) • [`firmware-analyst`](skills/firmware-analyst/SKILL.md) • [`flutter-expert`](skills/flutter-expert/SKILL.md) • [`frontend-developer`](skills/frontend-developer/SKILL.md) • [`frontend-mobile-development-component-scaffold`](skills/frontend-mobile-development-component-scaffold/SKILL.md) • [`go-concurrency-patterns`](skills/go-concurrency-patterns/SKILL.md) • [`godot-gdscript-patterns`](skills/godot-gdscript-patterns/SKILL.md) • [`golang-pro`](skills/golang-pro/SKILL.md) • [`haskell-pro`](skills/haskell-pro/SKILL.md) • [`ios-developer`](skills/ios-developer/SKILL.md) • [`java-pro`](skills/java-pro/SKILL.md) • [`javascript-pro`](skills/javascript-pro/SKILL.md) • [`javascript-testing-patterns`](skills/javascript-testing-patterns/SKILL.md) • [`javascript-typescript-typescript-scaffold`](skills/javascript-typescript-typescript-scaffold/SKILL.md) • [`managing-python-dependencies`](skills/managing-python-dependencies/SKILL.md) • [`mobile-developer`](skills/mobile-developer/SKILL.md) • [`modern-javascript-patterns`](skills/modern-javascript-patterns/SKILL.md) • [`mui`](skills/mui/SKILL.md) • [`nextjs-app-router-patterns`](skills/nextjs-app-router-patterns/SKILL.md) • [`nft-standards`](skills/nft-standards/SKILL.md) • [`nodejs-backend-patterns`](skills/nodejs-backend-patterns/SKILL.md) • [`openapi-spec-generation`](skills/openapi-spec-generation/SKILL.md) • [`openapi-to-typescript`](skills/openapi-to-typescript/SKILL.md) • [`php-pro`](skills/php-pro/SKILL.md) • [`posix-shell-pro`](skills/posix-shell-pro/SKILL.md) • [`python-development-python-scaffold`](skills/python-development-python-scaffold/SKILL.md) • [`python-packaging`](skills/python-packaging/SKILL.md) • [`python-performance-optimization`](skills/python-performance-optimization/SKILL.md) • [`python-pro`](skills/python-pro/SKILL.md) • [`python-testing-patterns`](skills/python-testing-patterns/SKILL.md) • [`react-dev`](skills/react-dev/SKILL.md) • [`react-modernization`](skills/react-modernization/SKILL.md) • [`react-state-management`](skills/react-state-management/SKILL.md) • [`react-useeffect`](skills/react-useeffect/SKILL.md) • [`ruby-pro`](skills/ruby-pro/SKILL.md) • [`rust-async-patterns`](skills/rust-async-patterns/SKILL.md) • [`rust-pro`](skills/rust-pro/SKILL.md) • [`scala-pro`](skills/scala-pro/SKILL.md) • [`shellcheck-configuration`](skills/shellcheck-configuration/SKILL.md) • [`tailwind-design-system`](skills/tailwind-design-system/SKILL.md) • [`temporal-python-pro`](skills/temporal-python-pro/SKILL.md) • [`temporal-python-testing`](skills/temporal-python-testing/SKILL.md) • [`typescript-advanced-types`](skills/typescript-advanced-types/SKILL.md) • [`typescript-pro`](skills/typescript-pro/SKILL.md) • [`unity-developer`](skills/unity-developer/SKILL.md) • [`unity-ecs-patterns`](skills/unity-ecs-patterns/SKILL.md) • [`uv-package-manager`](skills/uv-package-manager/SKILL.md) • [`web3-testing`](skills/web3-testing/SKILL.md) • [`webapp-testing`](skills/webapp-testing/SKILL.md)

### 📈 Business, Finance & Strategy
📁 *Full Documentation: [📈 Business, Finance & Strategy Document](categories/business_finance.md) (22 skills)*

[`billing-automation`](skills/billing-automation/SKILL.md) • [`business-analyst`](skills/business-analyst/SKILL.md) • [`content-marketer`](skills/content-marketer/SKILL.md) • [`customer-support`](skills/customer-support/SKILL.md) • [`employment-contract-templates`](skills/employment-contract-templates/SKILL.md) • [`hr-pro`](skills/hr-pro/SKILL.md) • [`legal-advisor`](skills/legal-advisor/SKILL.md) • [`market-sizing-analysis`](skills/market-sizing-analysis/SKILL.md) • [`payment-integration`](skills/payment-integration/SKILL.md) • [`paypal-integration`](skills/paypal-integration/SKILL.md) • [`quant-analyst`](skills/quant-analyst/SKILL.md) • [`risk-manager`](skills/risk-manager/SKILL.md) • [`risk-metrics-calculation`](skills/risk-metrics-calculation/SKILL.md) • [`sales-automator`](skills/sales-automator/SKILL.md) • [`seo-cannibalization-detector`](skills/seo-cannibalization-detector/SKILL.md) • [`seo-content-planner`](skills/seo-content-planner/SKILL.md) • [`seo-content-refresher`](skills/seo-content-refresher/SKILL.md) • [`seo-content-writer`](skills/seo-content-writer/SKILL.md) • [`seo-keyword-strategist`](skills/seo-keyword-strategist/SKILL.md) • [`seo-meta-optimizer`](skills/seo-meta-optimizer/SKILL.md) • [`seo-snippet-hunter`](skills/seo-snippet-hunter/SKILL.md) • [`stripe-integration`](skills/stripe-integration/SKILL.md)

### 🛠️ Development, Debugging & QA Workflows
📁 *Full Documentation: [🛠️ Development, Debugging & QA Workflows Document](categories/development_testing.md) (67 skills)*

[`adr-discovery`](skills/adr-discovery/SKILL.md) • [`adr-lifecycle-management`](skills/adr-lifecycle-management/SKILL.md) • [`application-performance-performance-optimization`](skills/application-performance-performance-optimization/SKILL.md) • [`backtesting-frameworks`](skills/backtesting-frameworks/SKILL.md) • [`changelog-automation`](skills/changelog-automation/SKILL.md) • [`changelog-generator`](skills/changelog-generator/SKILL.md) • [`code-refactoring-context-restore`](skills/code-refactoring-context-restore/SKILL.md) • [`code-refactoring-refactor-clean`](skills/code-refactoring-refactor-clean/SKILL.md) • [`code-refactoring-tech-debt`](skills/code-refactoring-tech-debt/SKILL.md) • [`code-review-excellence`](skills/code-review-excellence/SKILL.md) • [`code-reviewer`](skills/code-reviewer/SKILL.md) • [`codebase-cleanup-refactor-clean`](skills/codebase-cleanup-refactor-clean/SKILL.md) • [`codebase-cleanup-tech-debt`](skills/codebase-cleanup-tech-debt/SKILL.md) • [`commit-work`](skills/commit-work/SKILL.md) • [`comprehensive-review-full-review`](skills/comprehensive-review-full-review/SKILL.md) • [`comprehensive-review-pr-enhance`](skills/comprehensive-review-pr-enhance/SKILL.md) • [`conductor-implement`](skills/conductor-implement/SKILL.md) • [`conductor-manage`](skills/conductor-manage/SKILL.md) • [`conductor-new-track`](skills/conductor-new-track/SKILL.md) • [`conductor-revert`](skills/conductor-revert/SKILL.md) • [`conductor-setup`](skills/conductor-setup/SKILL.md) • [`conductor-status`](skills/conductor-status/SKILL.md) • [`conductor-validator`](skills/conductor-validator/SKILL.md) • [`context-driven-development`](skills/context-driven-development/SKILL.md) • [`context-management-context-restore`](skills/context-management-context-restore/SKILL.md) • [`context-management-context-save`](skills/context-management-context-save/SKILL.md) • [`context-manager`](skills/context-manager/SKILL.md) • [`custom-code-reviewer`](skills/custom-code-reviewer/SKILL.md) • [`debugger`](skills/debugger/SKILL.md) • [`debugging-strategies`](skills/debugging-strategies/SKILL.md) • [`dependency-lifecycle-orchestrator`](skills/dependency-lifecycle-orchestrator/SKILL.md) • [`dependency-updater`](skills/dependency-updater/SKILL.md) • [`dependency-upgrade`](skills/dependency-upgrade/SKILL.md) • [`distributed-debugging-debug-trace`](skills/distributed-debugging-debug-trace/SKILL.md) • [`dx-optimizer`](skills/dx-optimizer/SKILL.md) • [`e2e-testing-patterns`](skills/e2e-testing-patterns/SKILL.md) • [`error-debugging-error-analysis`](skills/error-debugging-error-analysis/SKILL.md) • [`error-debugging-error-trace`](skills/error-debugging-error-trace/SKILL.md) • [`error-detective`](skills/error-detective/SKILL.md) • [`error-diagnostics-error-analysis`](skills/error-diagnostics-error-analysis/SKILL.md) • [`error-diagnostics-error-trace`](skills/error-diagnostics-error-trace/SKILL.md) • [`error-diagnostics-orchestrator`](skills/error-diagnostics-orchestrator/SKILL.md) • [`error-handling-patterns`](skills/error-handling-patterns/SKILL.md) • [`git-pr-workflows-git-workflow`](skills/git-pr-workflows-git-workflow/SKILL.md) • [`git-pr-workflows-pr-enhance`](skills/git-pr-workflows-pr-enhance/SKILL.md) • [`install-adr-gatekeeper`](skills/install-adr-gatekeeper/SKILL.md) • [`mcp-builder`](skills/mcp-builder/SKILL.md) • [`memory-capture`](skills/memory-capture/SKILL.md) • [`memory-forensics`](skills/memory-forensics/SKILL.md) • [`memory-safety-patterns`](skills/memory-safety-patterns/SKILL.md) • [`performance-engineer`](skills/performance-engineer/SKILL.md) • [`performance-optimization-orchestrator`](skills/performance-optimization-orchestrator/SKILL.md) • [`qa-test-planner`](skills/qa-test-planner/SKILL.md) • [`reducing-entropy`](skills/reducing-entropy/SKILL.md) • [`screen-reader-testing`](skills/screen-reader-testing/SKILL.md) • [`skill-creator`](skills/skill-creator/SKILL.md) • [`skill-judge`](skills/skill-judge/SKILL.md) • [`skill-repair`](skills/skill-repair/SKILL.md) • [`tdd-orchestrator`](skills/tdd-orchestrator/SKILL.md) • [`tdd-workflows-tdd-cycle`](skills/tdd-workflows-tdd-cycle/SKILL.md) • [`tdd-workflows-tdd-green`](skills/tdd-workflows-tdd-green/SKILL.md) • [`tdd-workflows-tdd-red`](skills/tdd-workflows-tdd-red/SKILL.md) • [`tdd-workflows-tdd-refactor`](skills/tdd-workflows-tdd-refactor/SKILL.md) • [`team-collaboration-issue`](skills/team-collaboration-issue/SKILL.md) • [`template-skill`](skills/template-skill/SKILL.md) • [`test-automator`](skills/test-automator/SKILL.md) • [`unit-testing-test-generate`](skills/unit-testing-test-generate/SKILL.md)

### 💬 Productivity, Research & Communication
📁 *Full Documentation: [💬 Productivity, Research & Communication Document](categories/productivity_comms.md) (18 skills)*

[`content-research-writer`](skills/content-research-writer/SKILL.md) • [`daily-meeting-update`](skills/daily-meeting-update/SKILL.md) • [`difficult-workplace-conversations`](skills/difficult-workplace-conversations/SKILL.md) • [`domain-name-brainstormer`](skills/domain-name-brainstormer/SKILL.md) • [`feedback-mastery`](skills/feedback-mastery/SKILL.md) • [`file-organizer`](skills/file-organizer/SKILL.md) • [`humanizer`](skills/humanizer/SKILL.md) • [`internal-comms`](skills/internal-comms/SKILL.md) • [`lead-research-assistant`](skills/lead-research-assistant/SKILL.md) • [`lesson-learned`](skills/lesson-learned/SKILL.md) • [`meeting-insights-analyzer`](skills/meeting-insights-analyzer/SKILL.md) • [`naming-analyzer`](skills/naming-analyzer/SKILL.md) • [`professional-communication`](skills/professional-communication/SKILL.md) • [`raffle-winner-picker`](skills/raffle-winner-picker/SKILL.md) • [`session-handoff`](skills/session-handoff/SKILL.md) • [`team-collaboration-standup-notes`](skills/team-collaboration-standup-notes/SKILL.md) • [`tutorial-engineer`](skills/tutorial-engineer/SKILL.md) • [`writing-clearly-and-concisely`](skills/writing-clearly-and-concisely/SKILL.md)

### 📦 Other User Skills
📁 *Full Documentation: [Other User Skills Document](categories/other_user.md) (32 skills)*

[`cicd-automation-workflow-automate`](skills/cicd-automation-workflow-automate/SKILL.md) • [`codex`](skills/codex/SKILL.md) • [`command-creator`](skills/command-creator/SKILL.md) • [`competitive-ads-extractor`](skills/competitive-ads-extractor/SKILL.md) • [`competitive-landscape`](skills/competitive-landscape/SKILL.md) • [`crafting-effective-readmes`](skills/crafting-effective-readmes/SKILL.md) • [`git-advanced-workflows`](skills/git-advanced-workflows/SKILL.md) • [`jira`](skills/jira/SKILL.md) • [`julia-pro`](skills/julia-pro/SKILL.md) • [`kpi-dashboard-design`](skills/kpi-dashboard-design/SKILL.md) • [`legacy-modernizer`](skills/legacy-modernizer/SKILL.md) • [`mermaid-diagrams`](skills/mermaid-diagrams/SKILL.md) • [`mermaid-expert`](skills/mermaid-expert/SKILL.md) • [`minecraft-bukkit-pro`](skills/minecraft-bukkit-pro/SKILL.md) • [`multi-platform-apps-multi-platform`](skills/multi-platform-apps-multi-platform/SKILL.md) • [`nano-banana-pro`](skills/nano-banana-pro/SKILL.md) • [`notebook-guidance`](skills/notebook-guidance/SKILL.md) • [`parallax-landing-page`](skills/parallax-landing-page/SKILL.md) • [`perplexity`](skills/perplexity/SKILL.md) • [`plugin-forge`](skills/plugin-forge/SKILL.md) • [`projection-patterns`](skills/projection-patterns/SKILL.md) • [`protocol-reverse-engineering`](skills/protocol-reverse-engineering/SKILL.md) • [`reference-builder`](skills/reference-builder/SKILL.md) • [`reverse-engineer`](skills/reverse-engineer/SKILL.md) • [`search-specialist`](skills/search-specialist/SKILL.md) • [`ship-learn-next`](skills/ship-learn-next/SKILL.md) • [`team-composition-analysis`](skills/team-composition-analysis/SKILL.md) • [`track-management`](skills/track-management/SKILL.md) • [`ui-ux-designer`](skills/ui-ux-designer/SKILL.md) • [`ui-visual-validator`](skills/ui-visual-validator/SKILL.md) • [`workflow-orchestration-patterns`](skills/workflow-orchestration-patterns/SKILL.md) • [`workflow-patterns`](skills/workflow-patterns/SKILL.md)

