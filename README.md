# YUV AI Skills Repository

This repository is a comprehensive collection of AI "skills" designed for various AI harnesses, including Pi-agent, Gemini, and AI coding agent.

## Architecture

We use a dual-layered architecture to distinguish between fundamental building blocks and complex workflows:

### 1. Atomic Skills
**Location**: ` `
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

## Deployment

We provide a manifest-driven deployment system to package and deploy skills to different harnesses.

### Deployment Script
The `deploy_skills.py` script automates the following:
1. **Dependency Resolution**: Recursively identifies all required skills for a given harness.
2. **Package Generation**: Creates a deployment-ready directory (`deploy_package`) containing all necessary skills.
3. **Multi-Harness Support**: Supports `pi`, `gemini`, and `claude` configurations.

### Usage
To plan and generate a deployment package for the `pi` harness:
```bash
python3 deploy_skills.py --harness pi
```

## Project Structure
- ` `: Atomic skills categorized by domain.
- `manifest.json`: Machine-readable metadata for Composite skills.
- `audit_status.json`: Tracks the categorization and migration status of all skills.
- `deploy_skills.py`: The core deployment and packaging engine.
- `SKILL.md`: Documentation for every individual skill.

## Contributing
To add a new skill:
1. Determine if it is **Atomic** (add to ` `) or **Composite** (add to root).
2. Create a `SKILL.md` file describing the skill.
3. If Composite, create a `manifest.json` and list dependencies.
4. Update `audit_status.json` to reflect the new skill.


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
- **Architectural Decision Record**: See [ADR 0005: Local Memory RAG Architecture](adr/0005-local-memory-rag-architecture.md) for rationale.
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

This repository manages **828** modular AI skills across 12 primary domains.

### Overview

| Category | Skills | Quick Link |
|---|---|---|
| [🎨 Design, Film & Video](#-design-film-video) | **36** | [Full Doc ↗](categories/design_film_video.md) |
| [📄 Document & Media Processing](#-document-media-processing) | **12** | [Full Doc ↗](categories/document_media_processing.md) |
| [📓 Notion Integration](#-notion-integration) | **4** | [Full Doc ↗](categories/notion_integration.md) |
| [🤖 AI, RAG & LLM Engineering](#-ai-llm-engineering) | **29** | [Full Doc ↗](categories/ai_llm_engineering.md) |
| [🗄️ Databases & Data Engineering](#-databases-data) | **71** | [Full Doc ↗](categories/databases_data.md) |
| [🔒 Security, Compliance & Hardening](#-security-compliance) | **34** | [Full Doc ↗](categories/security_compliance.md) |
| [☁️ DevOps, Cloud & Infrastructure](#-devops-cloud) | **43** | [Full Doc ↗](categories/devops_cloud.md) |
| [🏗️ Architecture & Engineering Practices](#-software-architecture) | **31** | [Full Doc ↗](categories/software_architecture.md) |
| [💻 Software Engineering & Frameworks](#-software-languages) | **65** | [Full Doc ↗](categories/software_languages.md) |
| [📈 Business, Finance & Strategy](#-business-finance) | **22** | [Full Doc ↗](categories/business_finance.md) |
| [🛠️ Development, Debugging & QA Workflows](#-development-testing) | **68** | [Full Doc ↗](categories/development_testing.md) |
| [💬 Productivity, Research & Communication](#-productivity-comms) | **18** | [Full Doc ↗](categories/productivity_comms.md) |
| [📦 Other User Skills](#-other-user-skills) | **32** | [Full Doc ↗](categories/other_user.md) |

---

### 🎨 Design, Film & Video
📁 *Full Documentation: [🎨 Design, Film & Video Document](categories/design_film_video.md) (36 skills)*

[`algorithmic-art`](algorithmic-art/SKILL.md) • [`article-illustrations`](article-illustrations/SKILL.md) • [`artifacts-builder`](artifacts-builder/SKILL.md) • [`brand-guidelines`](brand-guidelines/SKILL.md) • [`canvas-design`](canvas-design/SKILL.md) • [`debugging-toolkit-smart-debug`](debugging-toolkit-smart-debug/SKILL.md) • [`design-system-starter`](design-system-starter/SKILL.md) • [`director`](director/SKILL.md) • [`draw-io`](draw-io/SKILL.md) • [`error-diagnostics-smart-debug`](error-diagnostics-smart-debug/SKILL.md) • [`excalidraw`](excalidraw/SKILL.md) • [`helm-chart-scaffolding`](helm-chart-scaffolding/SKILL.md) • [`hyperframes`](hyperframes/SKILL.md) • [`hyperframes-cli`](hyperframes-cli/SKILL.md) • [`hyperframes-registry`](hyperframes-registry/SKILL.md) • [`image-enhancer`](image-enhancer/SKILL.md) • [`incident-response-smart-fix`](incident-response-smart-fix/SKILL.md) • [`marp-slide`](marp-slide/SKILL.md) • [`meme-factory`](meme-factory/SKILL.md) • [`slack-gif-creator`](slack-gif-creator/SKILL.md) • [`startup-analyst`](startup-analyst/SKILL.md) • [`startup-business-analyst-business-case`](startup-business-analyst-business-case/SKILL.md) • [`startup-business-analyst-financial-projections`](startup-business-analyst-financial-projections/SKILL.md) • [`startup-business-analyst-market-opportunity`](startup-business-analyst-market-opportunity/SKILL.md) • [`startup-financial-modeling`](startup-financial-modeling/SKILL.md) • [`startup-metrics-framework`](startup-metrics-framework/SKILL.md) • [`theme-factory`](theme-factory/SKILL.md) • [`video-content-orchestrator`](video-content-orchestrator/SKILL.md) • [`video-downloader`](video-downloader/SKILL.md) • [`video-edit`](video-edit/SKILL.md) • [`video-to-landing-page`](video-to-landing-page/SKILL.md) • [`yuv-brand-orchestrator`](yuv-brand-orchestrator/SKILL.md) • [`yuv-decks`](yuv-decks/SKILL.md) • [`yuv-design-system`](yuv-design-system/SKILL.md) • [`yuv-pilot`](yuv-pilot/SKILL.md) • [`yuv-viral-video`](yuv-viral-video/SKILL.md)

### 📄 Document & Media Processing
📁 *Full Documentation: [📄 Document & Media Processing Document](categories/document_media_processing.md) (12 skills)*

[`api-documenter`](api-documenter/SKILL.md) • [`code-documentation-code-explain`](code-documentation-code-explain/SKILL.md) • [`code-documentation-doc-generate`](code-documentation-doc-generate/SKILL.md) • [`documentation-generation-doc-generate`](documentation-generation-doc-generate/SKILL.md) • [`docx`](docx/SKILL.md) • [`invoice-organizer`](invoice-organizer/SKILL.md) • [`notion-research-documentation`](notion-research-documentation/SKILL.md) • [`pdf`](pdf/SKILL.md) • [`pptx`](pptx/SKILL.md) • [`resemble-detect`](resemble-detect/SKILL.md) • [`web-to-markdown`](web-to-markdown/SKILL.md) • [`xlsx`](xlsx/SKILL.md)

### 📓 Notion Integration
📁 *Full Documentation: [📓 Notion Integration Document](categories/notion_integration.md) (4 skills)*

[`notion-intelligence-orchestrator`](notion-intelligence-orchestrator/SKILL.md) • [`notion-knowledge-capture`](notion-knowledge-capture/SKILL.md) • [`notion-meeting-intelligence`](notion-meeting-intelligence/SKILL.md) • [`notion-spec-to-implementation`](notion-spec-to-implementation/SKILL.md)

### 🤖 AI, RAG & LLM Engineering
📁 *Full Documentation: [🤖 AI, RAG & LLM Engineering Document](categories/ai_llm_engineering.md) (29 skills)*

[`agent-md-refactor`](agent-md-refactor/SKILL.md) • [`agent-orchestration-improve-agent`](agent-orchestration-improve-agent/SKILL.md) • [`agent-orchestration-multi-agent-optimize`](agent-orchestration-multi-agent-optimize/SKILL.md) • [`ai-engineer`](ai-engineer/SKILL.md) • [`cloud-sql-postgres-vectorassist`](cloud-sql-postgres-vectorassist/SKILL.md) • [`code-review-ai-ai-review`](code-review-ai-ai-review/SKILL.md) • [`embedding-strategies`](embedding-strategies/SKILL.md) • [`error-debugging-multi-agent-review`](error-debugging-multi-agent-review/SKILL.md) • [`gemini`](gemini/SKILL.md) • [`gepetto`](gepetto/SKILL.md) • [`hybrid-search-implementation`](hybrid-search-implementation/SKILL.md) • [`langchain-architecture`](langchain-architecture/SKILL.md) • [`llm-application-dev-ai-assistant`](llm-application-dev-ai-assistant/SKILL.md) • [`llm-application-dev-langchain-agent`](llm-application-dev-langchain-agent/SKILL.md) • [`llm-application-dev-prompt-optimize`](llm-application-dev-prompt-optimize/SKILL.md) • [`llm-evaluation`](llm-evaluation/SKILL.md) • [`machine-learning-ops-ml-pipeline`](machine-learning-ops-ml-pipeline/SKILL.md) • [`ml-best-practices`](ml-best-practices/SKILL.md) • [`ml-engineer`](ml-engineer/SKILL.md) • [`ml-pipeline-workflow`](ml-pipeline-workflow/SKILL.md) • [`mlops-engineer`](mlops-engineer/SKILL.md) • [`performance-testing-review-ai-review`](performance-testing-review-ai-review/SKILL.md) • [`performance-testing-review-multi-agent-review`](performance-testing-review-multi-agent-review/SKILL.md) • [`prompt-engineer`](prompt-engineer/SKILL.md) • [`prompt-engineering-patterns`](prompt-engineering-patterns/SKILL.md) • [`rag-implementation`](rag-implementation/SKILL.md) • [`similarity-search-patterns`](similarity-search-patterns/SKILL.md) • [`vector-database-engineer`](vector-database-engineer/SKILL.md) • [`vector-index-tuning`](vector-index-tuning/SKILL.md)

### 🗄️ Databases & Data Engineering
📁 *Full Documentation: [🗄️ Databases & Data Engineering Document](categories/databases_data.md) (71 skills)*

[`accidental-data-loss-prevention`](accidental-data-loss-prevention/SKILL.md) • [`airflow-dag-patterns`](airflow-dag-patterns/SKILL.md) • [`alloydb-omni-access-control`](alloydb-omni-access-control/SKILL.md) • [`alloydb-omni-container`](alloydb-omni-container/SKILL.md) • [`alloydb-omni-data`](alloydb-omni-data/SKILL.md) • [`alloydb-omni-health`](alloydb-omni-health/SKILL.md) • [`alloydb-omni-kubernetes`](alloydb-omni-kubernetes/SKILL.md) • [`alloydb-omni-monitor`](alloydb-omni-monitor/SKILL.md) • [`alloydb-omni-optimize`](alloydb-omni-optimize/SKILL.md) • [`alloydb-omni-performance`](alloydb-omni-performance/SKILL.md) • [`alloydb-omni-replication`](alloydb-omni-replication/SKILL.md) • [`alloydb-postgres-access-management`](alloydb-postgres-access-management/SKILL.md) • [`alloydb-postgres-admin`](alloydb-postgres-admin/SKILL.md) • [`alloydb-postgres-data`](alloydb-postgres-data/SKILL.md) • [`alloydb-postgres-health`](alloydb-postgres-health/SKILL.md) • [`alloydb-postgres-monitor`](alloydb-postgres-monitor/SKILL.md) • [`alloydb-postgres-optimize`](alloydb-postgres-optimize/SKILL.md) • [`alloydb-postgres-replication`](alloydb-postgres-replication/SKILL.md) • [`angular-migration`](angular-migration/SKILL.md) • [`bigquery`](bigquery/SKILL.md) • [`bigquery-data-transfer-service`](bigquery-data-transfer-service/SKILL.md) • [`building-data-apps`](building-data-apps/SKILL.md) • [`cloud-sql-mysql-admin`](cloud-sql-mysql-admin/SKILL.md) • [`cloud-sql-mysql-data`](cloud-sql-mysql-data/SKILL.md) • [`cloud-sql-mysql-lifecycle`](cloud-sql-mysql-lifecycle/SKILL.md) • [`cloud-sql-mysql-monitor`](cloud-sql-mysql-monitor/SKILL.md) • [`cloud-sql-postgres-admin`](cloud-sql-postgres-admin/SKILL.md) • [`cloud-sql-postgres-data`](cloud-sql-postgres-data/SKILL.md) • [`cloud-sql-postgres-health`](cloud-sql-postgres-health/SKILL.md) • [`cloud-sql-postgres-lifecycle`](cloud-sql-postgres-lifecycle/SKILL.md) • [`cloud-sql-postgres-monitor`](cloud-sql-postgres-monitor/SKILL.md) • [`cloud-sql-postgres-replication`](cloud-sql-postgres-replication/SKILL.md) • [`cloud-sql-postgres-view-config`](cloud-sql-postgres-view-config/SKILL.md) • [`cloud-sql-sqlserver-admin`](cloud-sql-sqlserver-admin/SKILL.md) • [`cloud-sql-sqlserver-data`](cloud-sql-sqlserver-data/SKILL.md) • [`cloud-sql-sqlserver-lifecycle`](cloud-sql-sqlserver-lifecycle/SKILL.md) • [`cloud-sql-sqlserver-monitor`](cloud-sql-sqlserver-monitor/SKILL.md) • [`data-autocleaning`](data-autocleaning/SKILL.md) • [`data-engineer`](data-engineer/SKILL.md) • [`data-engineering-data-driven-feature`](data-engineering-data-driven-feature/SKILL.md) • [`data-engineering-data-pipeline`](data-engineering-data-pipeline/SKILL.md) • [`data-quality-frameworks`](data-quality-frameworks/SKILL.md) • [`data-scientist`](data-scientist/SKILL.md) • [`data-storytelling`](data-storytelling/SKILL.md) • [`database-admin`](database-admin/SKILL.md) • [`database-architect`](database-architect/SKILL.md) • [`database-cloud-optimization-cost-optimize`](database-cloud-optimization-cost-optimize/SKILL.md) • [`database-migration`](database-migration/SKILL.md) • [`database-migrations-migration-observability`](database-migrations-migration-observability/SKILL.md) • [`database-migrations-sql-migrations`](database-migrations-sql-migrations/SKILL.md) • [`database-optimizer`](database-optimizer/SKILL.md) • [`database-schema-designer`](database-schema-designer/SKILL.md) • [`dataform-bigquery`](dataform-bigquery/SKILL.md) • [`dbt-bigquery`](dbt-bigquery/SKILL.md) • [`dbt-transformation-patterns`](dbt-transformation-patterns/SKILL.md) • [`discovering-gcp-data-assets`](discovering-gcp-data-assets/SKILL.md) • [`federate-lakehouse-catalog`](federate-lakehouse-catalog/SKILL.md) • [`firestore-data`](firestore-data/SKILL.md) • [`framework-migration-code-migrate`](framework-migration-code-migrate/SKILL.md) • [`framework-migration-deps-upgrade`](framework-migration-deps-upgrade/SKILL.md) • [`framework-migration-legacy-modernize`](framework-migration-legacy-modernize/SKILL.md) • [`gcp-data-pipelines`](gcp-data-pipelines/SKILL.md) • [`gcp-managed-airflow-migrations`](gcp-managed-airflow-migrations/SKILL.md) • [`gcp-spark`](gcp-spark/SKILL.md) • [`gcs-security-assessment`](gcs-security-assessment/SKILL.md) • [`gdpr-data-handling`](gdpr-data-handling/SKILL.md) • [`postgresql`](postgresql/SKILL.md) • [`spanner-data`](spanner-data/SKILL.md) • [`spark-optimization`](spark-optimization/SKILL.md) • [`sql-optimization-patterns`](sql-optimization-patterns/SKILL.md) • [`sql-pro`](sql-pro/SKILL.md)

### 🔒 Security, Compliance & Hardening
📁 *Full Documentation: [🔒 Security, Compliance & Hardening Document](categories/security_compliance.md) (34 skills)*

[`accessibility-compliance-accessibility-audit`](accessibility-compliance-accessibility-audit/SKILL.md) • [`adr-authoring`](adr-authoring/SKILL.md) • [`anti-reversing-techniques`](anti-reversing-techniques/SKILL.md) • [`attack-tree-construction`](attack-tree-construction/SKILL.md) • [`auth-implementation-patterns`](auth-implementation-patterns/SKILL.md) • [`backend-security-coder`](backend-security-coder/SKILL.md) • [`binary-analysis-patterns`](binary-analysis-patterns/SKILL.md) • [`codebase-cleanup-deps-audit`](codebase-cleanup-deps-audit/SKILL.md) • [`dependency-management-deps-audit`](dependency-management-deps-audit/SKILL.md) • [`frontend-mobile-security-xss-scan`](frontend-mobile-security-xss-scan/SKILL.md) • [`frontend-security-coder`](frontend-security-coder/SKILL.md) • [`gcloud-auth-verification`](gcloud-auth-verification/SKILL.md) • [`k8s-security-policies`](k8s-security-policies/SKILL.md) • [`malware-analyst`](malware-analyst/SKILL.md) • [`mobile-security-coder`](mobile-security-coder/SKILL.md) • [`mtls-configuration`](mtls-configuration/SKILL.md) • [`pci-compliance`](pci-compliance/SKILL.md) • [`sast-configuration`](sast-configuration/SKILL.md) • [`secrets-management`](secrets-management/SKILL.md) • [`security-auditor`](security-auditor/SKILL.md) • [`security-compliance-compliance-check`](security-compliance-compliance-check/SKILL.md) • [`security-governance-orchestrator`](security-governance-orchestrator/SKILL.md) • [`security-requirement-extraction`](security-requirement-extraction/SKILL.md) • [`security-scanning-security-dependencies`](security-scanning-security-dependencies/SKILL.md) • [`security-scanning-security-hardening`](security-scanning-security-hardening/SKILL.md) • [`security-scanning-security-sast`](security-scanning-security-sast/SKILL.md) • [`security-tech-debt`](security-tech-debt/SKILL.md) • [`seo-authority-builder`](seo-authority-builder/SKILL.md) • [`seo-content-auditor`](seo-content-auditor/SKILL.md) • [`solidity-security`](solidity-security/SKILL.md) • [`stride-analysis-patterns`](stride-analysis-patterns/SKILL.md) • [`threat-mitigation-mapping`](threat-mitigation-mapping/SKILL.md) • [`threat-modeling-expert`](threat-modeling-expert/SKILL.md) • [`wcag-audit-patterns`](wcag-audit-patterns/SKILL.md)

### ☁️ DevOps, Cloud & Infrastructure
📁 *Full Documentation: [☁️ DevOps, Cloud & Infrastructure Document](categories/devops_cloud.md) (43 skills)*

[`api-testing-observability-api-mock`](api-testing-observability-api-mock/SKILL.md) • [`bazel-build-optimization`](bazel-build-optimization/SKILL.md) • [`c4-container`](c4-container/SKILL.md) • [`cost-optimization`](cost-optimization/SKILL.md) • [`datadog-cli`](datadog-cli/SKILL.md) • [`deployment-engineer`](deployment-engineer/SKILL.md) • [`deployment-pipeline-design`](deployment-pipeline-design/SKILL.md) • [`deployment-validation-config-validate`](deployment-validation-config-validate/SKILL.md) • [`devops-troubleshooter`](devops-troubleshooter/SKILL.md) • [`distributed-tracing`](distributed-tracing/SKILL.md) • [`gcp-composer-troubleshooting`](gcp-composer-troubleshooting/SKILL.md) • [`gcp-dataflow`](gcp-dataflow/SKILL.md) • [`gcp-pipeline-orchestration`](gcp-pipeline-orchestration/SKILL.md) • [`gcp-pipeline-resource-provisioning`](gcp-pipeline-resource-provisioning/SKILL.md) • [`github-actions-node24`](github-actions-node24/SKILL.md) • [`github-actions-templates`](github-actions-templates/SKILL.md) • [`gitlab-ci-patterns`](gitlab-ci-patterns/SKILL.md) • [`gitops-workflow`](gitops-workflow/SKILL.md) • [`grafana-dashboards`](grafana-dashboards/SKILL.md) • [`hybrid-cloud-networking`](hybrid-cloud-networking/SKILL.md) • [`incident-responder`](incident-responder/SKILL.md) • [`incident-response-incident-response`](incident-response-incident-response/SKILL.md) • [`incident-runbook-templates`](incident-runbook-templates/SKILL.md) • [`istio-traffic-management`](istio-traffic-management/SKILL.md) • [`k8s-manifest-generator`](k8s-manifest-generator/SKILL.md) • [`kubernetes-architect`](kubernetes-architect/SKILL.md) • [`linkerd-patterns`](linkerd-patterns/SKILL.md) • [`monorepo-architect`](monorepo-architect/SKILL.md) • [`monorepo-management`](monorepo-management/SKILL.md) • [`network-engineer`](network-engineer/SKILL.md) • [`nx-workspace-patterns`](nx-workspace-patterns/SKILL.md) • [`observability-engineer`](observability-engineer/SKILL.md) • [`observability-monitoring-monitor-setup`](observability-monitoring-monitor-setup/SKILL.md) • [`observability-monitoring-slo-implement`](observability-monitoring-slo-implement/SKILL.md) • [`on-call-handoff-patterns`](on-call-handoff-patterns/SKILL.md) • [`postmortem-writing`](postmortem-writing/SKILL.md) • [`prometheus-configuration`](prometheus-configuration/SKILL.md) • [`service-mesh-expert`](service-mesh-expert/SKILL.md) • [`service-mesh-observability`](service-mesh-observability/SKILL.md) • [`slo-implementation`](slo-implementation/SKILL.md) • [`terraform-module-library`](terraform-module-library/SKILL.md) • [`terraform-specialist`](terraform-specialist/SKILL.md) • [`turborepo-caching`](turborepo-caching/SKILL.md)

### 🏗️ Architecture & Engineering Practices
📁 *Full Documentation: [🏗️ Architecture & Engineering Practices Document](categories/software_architecture.md) (31 skills)*

[`architect-review`](architect-review/SKILL.md) • [`architecture-decision-records`](architecture-decision-records/SKILL.md) • [`architecture-governance-orchestrator`](architecture-governance-orchestrator/SKILL.md) • [`architecture-patterns`](architecture-patterns/SKILL.md) • [`backend-architect`](backend-architect/SKILL.md) • [`backend-development-feature-development`](backend-development-feature-development/SKILL.md) • [`c4-architecture`](c4-architecture/SKILL.md) • [`c4-architecture-c4-architecture`](c4-architecture-c4-architecture/SKILL.md) • [`c4-code`](c4-code/SKILL.md) • [`c4-component`](c4-component/SKILL.md) • [`c4-context`](c4-context/SKILL.md) • [`cloud-architect`](cloud-architect/SKILL.md) • [`content-governance-orchestrator`](content-governance-orchestrator/SKILL.md) • [`cqrs-implementation`](cqrs-implementation/SKILL.md) • [`docs-architect`](docs-architect/SKILL.md) • [`dotnet-architect`](dotnet-architect/SKILL.md) • [`event-sourcing-architect`](event-sourcing-architect/SKILL.md) • [`event-store-design`](event-store-design/SKILL.md) • [`frontend-to-backend-requirements`](frontend-to-backend-requirements/SKILL.md) • [`full-stack-orchestration-full-stack-feature`](full-stack-orchestration-full-stack-feature/SKILL.md) • [`game-changing-features`](game-changing-features/SKILL.md) • [`git-pr-workflows-onboard`](git-pr-workflows-onboard/SKILL.md) • [`graphql-architect`](graphql-architect/SKILL.md) • [`hybrid-cloud-architect`](hybrid-cloud-architect/SKILL.md) • [`microservices-patterns`](microservices-patterns/SKILL.md) • [`multi-cloud-architecture`](multi-cloud-architecture/SKILL.md) • [`react-native-architecture`](react-native-architecture/SKILL.md) • [`requirements-clarity`](requirements-clarity/SKILL.md) • [`saga-orchestration`](saga-orchestration/SKILL.md) • [`seo-structure-architect`](seo-structure-architect/SKILL.md) • [`systems-programming-rust-project`](systems-programming-rust-project/SKILL.md)

### 💻 Software Engineering & Frameworks
📁 *Full Documentation: [💻 Software Engineering & Frameworks Document](categories/software_languages.md) (65 skills)*

[`api-design-principles`](api-design-principles/SKILL.md) • [`arm-cortex-expert`](arm-cortex-expert/SKILL.md) • [`async-python-patterns`](async-python-patterns/SKILL.md) • [`backend-to-frontend-handoff-docs`](backend-to-frontend-handoff-docs/SKILL.md) • [`bash-defensive-patterns`](bash-defensive-patterns/SKILL.md) • [`bash-pro`](bash-pro/SKILL.md) • [`bats-testing-patterns`](bats-testing-patterns/SKILL.md) • [`blockchain-developer`](blockchain-developer/SKILL.md) • [`c-pro`](c-pro/SKILL.md) • [`cpp-pro`](cpp-pro/SKILL.md) • [`csharp-pro`](csharp-pro/SKILL.md) • [`defi-protocol-templates`](defi-protocol-templates/SKILL.md) • [`django-pro`](django-pro/SKILL.md) • [`dotnet-backend-patterns`](dotnet-backend-patterns/SKILL.md) • [`elixir-pro`](elixir-pro/SKILL.md) • [`fastapi-pro`](fastapi-pro/SKILL.md) • [`fastapi-templates`](fastapi-templates/SKILL.md) • [`firmware-analyst`](firmware-analyst/SKILL.md) • [`flutter-expert`](flutter-expert/SKILL.md) • [`frontend-developer`](frontend-developer/SKILL.md) • [`frontend-mobile-development-component-scaffold`](frontend-mobile-development-component-scaffold/SKILL.md) • [`go-concurrency-patterns`](go-concurrency-patterns/SKILL.md) • [`godot-gdscript-patterns`](godot-gdscript-patterns/SKILL.md) • [`golang-pro`](golang-pro/SKILL.md) • [`haskell-pro`](haskell-pro/SKILL.md) • [`ios-developer`](ios-developer/SKILL.md) • [`java-pro`](java-pro/SKILL.md) • [`javascript-pro`](javascript-pro/SKILL.md) • [`javascript-testing-patterns`](javascript-testing-patterns/SKILL.md) • [`javascript-typescript-typescript-scaffold`](javascript-typescript-typescript-scaffold/SKILL.md) • [`managing-python-dependencies`](managing-python-dependencies/SKILL.md) • [`mobile-developer`](mobile-developer/SKILL.md) • [`modern-javascript-patterns`](modern-javascript-patterns/SKILL.md) • [`mui`](mui/SKILL.md) • [`nextjs-app-router-patterns`](nextjs-app-router-patterns/SKILL.md) • [`nft-standards`](nft-standards/SKILL.md) • [`nodejs-backend-patterns`](nodejs-backend-patterns/SKILL.md) • [`openapi-spec-generation`](openapi-spec-generation/SKILL.md) • [`openapi-to-typescript`](openapi-to-typescript/SKILL.md) • [`php-pro`](php-pro/SKILL.md) • [`posix-shell-pro`](posix-shell-pro/SKILL.md) • [`python-development-python-scaffold`](python-development-python-scaffold/SKILL.md) • [`python-packaging`](python-packaging/SKILL.md) • [`python-performance-optimization`](python-performance-optimization/SKILL.md) • [`python-pro`](python-pro/SKILL.md) • [`python-testing-patterns`](python-testing-patterns/SKILL.md) • [`react-dev`](react-dev/SKILL.md) • [`react-modernization`](react-modernization/SKILL.md) • [`react-state-management`](react-state-management/SKILL.md) • [`react-useeffect`](react-useeffect/SKILL.md) • [`ruby-pro`](ruby-pro/SKILL.md) • [`rust-async-patterns`](rust-async-patterns/SKILL.md) • [`rust-pro`](rust-pro/SKILL.md) • [`scala-pro`](scala-pro/SKILL.md) • [`shellcheck-configuration`](shellcheck-configuration/SKILL.md) • [`tailwind-design-system`](tailwind-design-system/SKILL.md) • [`temporal-python-pro`](temporal-python-pro/SKILL.md) • [`temporal-python-testing`](temporal-python-testing/SKILL.md) • [`typescript-advanced-types`](typescript-advanced-types/SKILL.md) • [`typescript-pro`](typescript-pro/SKILL.md) • [`unity-developer`](unity-developer/SKILL.md) • [`unity-ecs-patterns`](unity-ecs-patterns/SKILL.md) • [`uv-package-manager`](uv-package-manager/SKILL.md) • [`web3-testing`](web3-testing/SKILL.md) • [`webapp-testing`](webapp-testing/SKILL.md)

### 📈 Business, Finance & Strategy
📁 *Full Documentation: [📈 Business, Finance & Strategy Document](categories/business_finance.md) (22 skills)*

[`billing-automation`](billing-automation/SKILL.md) • [`business-analyst`](business-analyst/SKILL.md) • [`content-marketer`](content-marketer/SKILL.md) • [`customer-support`](customer-support/SKILL.md) • [`employment-contract-templates`](employment-contract-templates/SKILL.md) • [`hr-pro`](hr-pro/SKILL.md) • [`legal-advisor`](legal-advisor/SKILL.md) • [`market-sizing-analysis`](market-sizing-analysis/SKILL.md) • [`payment-integration`](payment-integration/SKILL.md) • [`paypal-integration`](paypal-integration/SKILL.md) • [`quant-analyst`](quant-analyst/SKILL.md) • [`risk-manager`](risk-manager/SKILL.md) • [`risk-metrics-calculation`](risk-metrics-calculation/SKILL.md) • [`sales-automator`](sales-automator/SKILL.md) • [`seo-cannibalization-detector`](seo-cannibalization-detector/SKILL.md) • [`seo-content-planner`](seo-content-planner/SKILL.md) • [`seo-content-refresher`](seo-content-refresher/SKILL.md) • [`seo-content-writer`](seo-content-writer/SKILL.md) • [`seo-keyword-strategist`](seo-keyword-strategist/SKILL.md) • [`seo-meta-optimizer`](seo-meta-optimizer/SKILL.md) • [`seo-snippet-hunter`](seo-snippet-hunter/SKILL.md) • [`stripe-integration`](stripe-integration/SKILL.md)

### 🛠️ Development, Debugging & QA Workflows
📁 *Full Documentation: [🛠️ Development, Debugging & QA Workflows Document](categories/development_testing.md) (68 skills)*

[`adr-discovery`](adr-discovery/SKILL.md) • [`adr-gatekeeper`](adr-gatekeeper/SKILL.md) • [`adr-lifecycle-management`](adr-lifecycle-management/SKILL.md) • [`application-performance-performance-optimization`](application-performance-performance-optimization/SKILL.md) • [`backtesting-frameworks`](backtesting-frameworks/SKILL.md) • [`changelog-automation`](changelog-automation/SKILL.md) • [`changelog-generator`](changelog-generator/SKILL.md) • [`code-refactoring-context-restore`](code-refactoring-context-restore/SKILL.md) • [`code-refactoring-refactor-clean`](code-refactoring-refactor-clean/SKILL.md) • [`code-refactoring-tech-debt`](code-refactoring-tech-debt/SKILL.md) • [`code-review-excellence`](code-review-excellence/SKILL.md) • [`code-reviewer`](code-reviewer/SKILL.md) • [`codebase-cleanup-refactor-clean`](codebase-cleanup-refactor-clean/SKILL.md) • [`codebase-cleanup-tech-debt`](codebase-cleanup-tech-debt/SKILL.md) • [`commit-work`](commit-work/SKILL.md) • [`comprehensive-review-full-review`](comprehensive-review-full-review/SKILL.md) • [`comprehensive-review-pr-enhance`](comprehensive-review-pr-enhance/SKILL.md) • [`conductor-implement`](conductor-implement/SKILL.md) • [`conductor-manage`](conductor-manage/SKILL.md) • [`conductor-new-track`](conductor-new-track/SKILL.md) • [`conductor-revert`](conductor-revert/SKILL.md) • [`conductor-setup`](conductor-setup/SKILL.md) • [`conductor-status`](conductor-status/SKILL.md) • [`conductor-validator`](conductor-validator/SKILL.md) • [`context-driven-development`](context-driven-development/SKILL.md) • [`context-management-context-restore`](context-management-context-restore/SKILL.md) • [`context-management-context-save`](context-management-context-save/SKILL.md) • [`context-manager`](context-manager/SKILL.md) • [`custom-code-reviewer`](custom-code-reviewer/SKILL.md) • [`debugger`](debugger/SKILL.md) • [`debugging-strategies`](debugging-strategies/SKILL.md) • [`dependency-lifecycle-orchestrator`](dependency-lifecycle-orchestrator/SKILL.md) • [`dependency-updater`](dependency-updater/SKILL.md) • [`dependency-upgrade`](dependency-upgrade/SKILL.md) • [`distributed-debugging-debug-trace`](distributed-debugging-debug-trace/SKILL.md) • [`dx-optimizer`](dx-optimizer/SKILL.md) • [`e2e-testing-patterns`](e2e-testing-patterns/SKILL.md) • [`error-debugging-error-analysis`](error-debugging-error-analysis/SKILL.md) • [`error-debugging-error-trace`](error-debugging-error-trace/SKILL.md) • [`error-detective`](error-detective/SKILL.md) • [`error-diagnostics-error-analysis`](error-diagnostics-error-analysis/SKILL.md) • [`error-diagnostics-error-trace`](error-diagnostics-error-trace/SKILL.md) • [`error-diagnostics-orchestrator`](error-diagnostics-orchestrator/SKILL.md) • [`error-handling-patterns`](error-handling-patterns/SKILL.md) • [`git-pr-workflows-git-workflow`](git-pr-workflows-git-workflow/SKILL.md) • [`git-pr-workflows-pr-enhance`](git-pr-workflows-pr-enhance/SKILL.md) • [`install-adr-gatekeeper`](install-adr-gatekeeper/SKILL.md) • [`mcp-builder`](mcp-builder/SKILL.md) • [`memory-capture`](memory-capture/SKILL.md) • [`memory-forensics`](memory-forensics/SKILL.md) • [`memory-safety-patterns`](memory-safety-patterns/SKILL.md) • [`performance-engineer`](performance-engineer/SKILL.md) • [`performance-optimization-orchestrator`](performance-optimization-orchestrator/SKILL.md) • [`qa-test-planner`](qa-test-planner/SKILL.md) • [`reducing-entropy`](reducing-entropy/SKILL.md) • [`screen-reader-testing`](screen-reader-testing/SKILL.md) • [`skill-creator`](skill-creator/SKILL.md) • [`skill-judge`](skill-judge/SKILL.md) • [`skill-repair`](skill-repair/SKILL.md) • [`tdd-orchestrator`](tdd-orchestrator/SKILL.md) • [`tdd-workflows-tdd-cycle`](tdd-workflows-tdd-cycle/SKILL.md) • [`tdd-workflows-tdd-green`](tdd-workflows-tdd-green/SKILL.md) • [`tdd-workflows-tdd-red`](tdd-workflows-tdd-red/SKILL.md) • [`tdd-workflows-tdd-refactor`](tdd-workflows-tdd-refactor/SKILL.md) • [`team-collaboration-issue`](team-collaboration-issue/SKILL.md) • [`template-skill`](template-skill/SKILL.md) • [`test-automator`](test-automator/SKILL.md) • [`unit-testing-test-generate`](unit-testing-test-generate/SKILL.md)

### 💬 Productivity, Research & Communication
📁 *Full Documentation: [💬 Productivity, Research & Communication Document](categories/productivity_comms.md) (18 skills)*

[`content-research-writer`](content-research-writer/SKILL.md) • [`daily-meeting-update`](daily-meeting-update/SKILL.md) • [`difficult-workplace-conversations`](difficult-workplace-conversations/SKILL.md) • [`domain-name-brainstormer`](domain-name-brainstormer/SKILL.md) • [`feedback-mastery`](feedback-mastery/SKILL.md) • [`file-organizer`](file-organizer/SKILL.md) • [`humanizer`](humanizer/SKILL.md) • [`internal-comms`](internal-comms/SKILL.md) • [`lead-research-assistant`](lead-research-assistant/SKILL.md) • [`lesson-learned`](lesson-learned/SKILL.md) • [`meeting-insights-analyzer`](meeting-insights-analyzer/SKILL.md) • [`naming-analyzer`](naming-analyzer/SKILL.md) • [`professional-communication`](professional-communication/SKILL.md) • [`raffle-winner-picker`](raffle-winner-picker/SKILL.md) • [`session-handoff`](session-handoff/SKILL.md) • [`team-collaboration-standup-notes`](team-collaboration-standup-notes/SKILL.md) • [`tutorial-engineer`](tutorial-engineer/SKILL.md) • [`writing-clearly-and-concisely`](writing-clearly-and-concisely/SKILL.md)

### 📦 Other User Skills
📁 *Full Documentation: [Other User Skills Document](categories/other_user.md) (32 skills)*

[`cicd-automation-workflow-automate`](cicd-automation-workflow-automate/SKILL.md) • [`codex`](codex/SKILL.md) • [`command-creator`](command-creator/SKILL.md) • [`competitive-ads-extractor`](competitive-ads-extractor/SKILL.md) • [`competitive-landscape`](competitive-landscape/SKILL.md) • [`crafting-effective-readmes`](crafting-effective-readmes/SKILL.md) • [`git-advanced-workflows`](git-advanced-workflows/SKILL.md) • [`jira`](jira/SKILL.md) • [`julia-pro`](julia-pro/SKILL.md) • [`kpi-dashboard-design`](kpi-dashboard-design/SKILL.md) • [`legacy-modernizer`](legacy-modernizer/SKILL.md) • [`mermaid-diagrams`](mermaid-diagrams/SKILL.md) • [`mermaid-expert`](mermaid-expert/SKILL.md) • [`minecraft-bukkit-pro`](minecraft-bukkit-pro/SKILL.md) • [`multi-platform-apps-multi-platform`](multi-platform-apps-multi-platform/SKILL.md) • [`nano-banana-pro`](nano-banana-pro/SKILL.md) • [`notebook-guidance`](notebook-guidance/SKILL.md) • [`parallax-landing-page`](parallax-landing-page/SKILL.md) • [`perplexity`](perplexity/SKILL.md) • [`plugin-forge`](plugin-forge/SKILL.md) • [`projection-patterns`](projection-patterns/SKILL.md) • [`protocol-reverse-engineering`](protocol-reverse-engineering/SKILL.md) • [`reference-builder`](reference-builder/SKILL.md) • [`reverse-engineer`](reverse-engineer/SKILL.md) • [`search-specialist`](search-specialist/SKILL.md) • [`ship-learn-next`](ship-learn-next/SKILL.md) • [`team-composition-analysis`](team-composition-analysis/SKILL.md) • [`track-management`](track-management/SKILL.md) • [`ui-ux-designer`](ui-ux-designer/SKILL.md) • [`ui-visual-validator`](ui-visual-validator/SKILL.md) • [`workflow-orchestration-patterns`](workflow-orchestration-patterns/SKILL.md) • [`workflow-patterns`](workflow-patterns/SKILL.md)

