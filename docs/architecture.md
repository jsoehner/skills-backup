# Current State of Architecture & Governance Strategy

## Overview
The system is designed as a high-performance, scalable, and maintainable platform leveraging a modern cloud-native stack. It emphasizes local-first memory management, robust architectural governance, and a consistent brand identity.

## Core Technology Stack
- **Frontend**: Next.js 15 / React 19 with Tailwind CSS.
- **Backend**: Python 3.12+ with FastAPI.
- **Primary Database**: PostgreSQL (ACID compliant, relational).
- **Caching**: Redis (high-speed key-value storage).
- **Local Memory**: LanceDB with `sentence-transformers` for local, free, and performant vector search and semantic memory.
- **Orchestration**: Kubernetes for container orchestration and Temporal for durable workflow management.

## Architectural Patterns
- **Monorepo Management**: Managed via Nx/Turborepo for efficient builds and shared dependency handling.
- **Design Patterns**: Implements Clean Architecture, Hexagonal Architecture, and Domain-Driven Design (DDD) principles.
- **Workflow Orchestration**: Temporal-based saga patterns for distributed transactions and long-running processes.
- **Architecture Governance**: Decision-making is formalized through Architecture Decision Records (ADRs) and C4 modeling.

## Brand & Design System
- **Identity**: YUV.AI brand identity.
- **Design System**: Custom-built system including design tokens, component libraries, and accessibility standards.
- **Visual Language**: "Fly High" motifs, phoenix mark, and specific color palettes (Neon, Decks, Warm Editorial).

## Memory & Context Management
- **Local-First**: Replaced paid cloud-based vector services with a local LanceDB implementation.
- **Batch Consolidation**: Active process of consolidating skills and memories to optimize context window usage and reduce token costs.
- **Session Handoff**: Structured system for transferring state between AI agent sessions.

## Roadmap & Governance Overview
- **ADRs**: All significant technical decisions are logged in the [`docs/adr/`](adr/README.md) directory.
- **Documentation**: Automated and manual documentation generation for APIs, runbooks, and system diagrams.
- **Security**: Integrated SAST, threat modeling, and compliance checks (GDPR, etc.).

---

# 🏛️ Architectural Decision Record (ADR) Governance Strategy

## 1. Executive Summary
The goal of this governance strategy is to eliminate "Architecture by Accident"—where the system's design evolves through undocumented, localized decisions that leave future engineers guessing at the "why" behind the "what." 

By utilizing the **ADR Skill Trilogy**, we establish a systematic pipeline to identify, document, and maintain the architectural integrity of our codebase directly within [`docs/adr/`](adr/README.md).

## 2. The ADR Skill Trilogy: A Unified Pipeline
We treat ADR management as a three-stage pipeline. Each skill serves a distinct functional role:

### Phase 1: Discovery (The Filter)
**Skill**: [`adr-discovery`](../skills/adr-discovery/SKILL.md)
*   **Role**: The Gatekeeper.
*   **Function**: Prevents "ADR Bloat" by filtering out trivial changes (e.g., variable naming, local refactors) and identifying **Architecturally Significant Requirements (ASRs)**.
*   **Trigger**: Run during the design phase of a feature or during the review of a high-impact Pull Request.

### Phase 2: Authoring (The Standard)
**Skill**: [`adr-authoring`](../skills/adr-authoring/SKILL.md)
*   **Role**: The Creator.
*   **Function**: Ensures that once a decision is identified as significant, it is captured in a high-quality, consistent format using templates in [`docs/adr/templates/`](adr/templates/) that prioritize **Consequences** over mere Rationale.
*   **Trigger**: Run immediately after `adr-discovery` confirms a record is needed.

### Phase 3: Lifecycle (The Continuity)
**Skill**: [`adr-lifecycle-management`](../skills/adr-lifecycle-management/SKILL.md)
*   **Role**: The Maintainer.
*   **Function**: Ensures the decision log in [`docs/adr/README.md`](adr/README.md) remains a living document. It manages status transitions and enforces bidirectional linking to preserve the historical path of the architecture.
*   **Trigger**: Run whenever a decision is implemented, superseded by a newer choice, or retired.

---

## 3. Governance Logic: Constraints vs. Freedom
To balance engineering velocity with architectural integrity, each skill employs a "Freedom Calibration."

| Skill | Constraint Level | High Rigidity (Non-Negotiable) | High Freedom (Flexible) | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Discovery** | **Medium** | Must follow ASR categories (Quality Attributes, Constraints, Debt). | Scoring and impact evaluation can be tailored to project size. | Ensures we catch the *right* things while allowing for different project scales. |
| **Authoring** | **Medium** | Must contain Context, Decision, and Consequences. | Choice of template ([Minimum](adr/templates/Minimum_ADR_Template.md), [Standard](adr/templates/Standard_ADR_Template.md), [Comprehensive](adr/templates/Comprehensive_ADR_Template.md)) is matched to risk. | Guarantees utility for the reader while respecting developer preference for tools. |
| **Lifecycle** | **High** | **Bidirectional linking** and the **"Never Delete"** rule. | The method of indexing (manual table vs. auto-gen) is flexible. | Historical integrity is paramount. We must never lose the "why" of past decisions. |

---

## 4. Operational Workflow
To implement this strategy, engineers should follow this standard operating procedure:

### Step 1: The Design Check (`adr-discovery`)
Before starting a major feature or infrastructure change, run the `adr-discovery` skill.
*   **Question**: "Does this change affect scalability, security, cost, or long-term maintainability?"
*   **Action**: If **Yes**, proceed to Step 2. If **No**, document the rationale briefly in the PR/Issue and proceed with development.

### Step 2: The Drafting Phase (`adr-authoring`)
Once a decision is flagged as significant:
1.  Use `adr-authoring` to select the appropriate template from `docs/adr/templates/`.
2.  Draft the ADR in `docs/adr/NNNN-title.md`, ensuring the **Consequences** section is honest and detailed (including the downsides).
3.  Submit the ADR for review as part of the technical design approval.

### Step 3: The Maintenance Loop (`adr-lifecycle-management`)
Once the decision is live and the project evolves:
1.  **New Decision?** Create a new ADR in `docs/adr/` and use the lifecycle skill to update the index ([`docs/adr/README.md`](adr/README.md)).
2.  **Superseding a Decision?** Use the lifecycle skill to create the bidirectional link between the old and new records in `docs/adr/`.
3.  **Retiring a Decision?** Mark as `Deprecated` or `Superseded`; never delete the file.

---

## 5. Success Metrics & Integrity Rules
*   **Traceability**: Can a new engineer find the "why" for a core system component in under 2 minutes?
*   **Consistency**: Do all ADRs follow a recognizable structure in `docs/adr/`?
*   **Integrity**: Are there any "orphaned" decisions (decisions with no links to what superseded them)?
*   **Immutability**: Approved decisions are append-only. Never modify historical records in place.

---

## 6. Automated Enforcement: Deploying `install-adr-gatekeeper`

To prevent architectural drift automatically, repositories deploy the [`install-adr-gatekeeper`](../skills/install-adr-gatekeeper/SKILL.md) skill:

1. **Deploying the Gatekeeper**:
   ```bash
   # Run the install-adr-gatekeeper skill to provision gatekeeping assets:
   # - docs/adr/adr_index.json
   # - docs/adr/adr_analyst_config.json
   # - docs/adr/adr_analyst_prompt.txt
   # - scripts/adr_gatekeeper.py
   # - .github/workflows/adr-gatekeeper.yml
   # - .git/hooks/pre-commit
   ```

2. **Local Pre-Commit Guard**:
   When developers stage modifications to core infrastructure, schema definitions, or framework configurations, the local hook validates that an ADR in `docs/adr/` is included in the commit.

3. **CI/CD Pull Request Gate**:
   GitHub Actions executes `scripts/adr_gatekeeper.py <base_branch>` on every PR. If an architecturally sensitive path is modified without an ADR in `docs/adr/`, the build fails and provides actionable instructions on drafting the record.
