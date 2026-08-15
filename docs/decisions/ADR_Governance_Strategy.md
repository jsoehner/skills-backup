# Architectural Decision Record (ADR) Governance Strategy

## 1. Executive Summary
The goal of this governance strategy is to eliminate "Architecture by Accident"—where the system's design evolves through undocumented, localized decisions that leave future engineers guessing at the "why" behind the "what." 

By utilizing the **ADR Skill Trilogy**, we establish a systematic pipeline to identify, document, and maintain the architectural integrity of our codebase.

## 2. The ADR Skill Trilogy: A Unified Pipeline
We treat ADR management as a three-stage pipeline. Each skill serves a distinct functional role:

### Phase 1: Discovery (The Filter)
**Skill**: `adr-discovery`
*   **Role**: The Gatekeeper.
*   **Function**: Prevents "ADR Bloat" by filtering out trivial changes (e.g., variable naming, local refactors) and identifying **Architecturally Significant Requirements (ASRs)**.
*   **Trigger**: Run during the design phase of a feature or during the review of a high-impact Pull Request.

### Phase 2: Authoring (The Standard)
**Skill**: `adr-authoring`
*   **Role**: The Creator.
*   **Function**: Ensures that once a decision is identified as significant, it is captured in a high-quality, consistent format that prioritizes **Consequences** over mere Rationale.
*   **Trigger**: Run immediately after `adr-discovery` confirms a record is needed.

### Phase 3: Lifecycle (The Continuity)
**Skill**: `adr-lifecycle-management`
*   **Role**: The Maintainer.
*   **Function**: Ensures the decision log remains a "living" document. It manages status transitions and enforces bidirectional linking to preserve the historical path of the architecture.
*   **Trigger**: Run whenever a decision is implemented, superseded by a newer choice, or retired.

---

## 3. Governance Logic: Constraints vs. Freedom
To balance engineering velocity with architectural integrity, each skill employs a "Freedom Calibration."

| Skill | Constraint Level | High Rigidity (Non-Negotiable) | High Freedom (Flexible) | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Discovery** | **Medium** | Must follow ASR categories (Quality Attributes, Constraints, Debt). | Scoring and impact evaluation can be tailored to project size. | Ensures we catch the *right* things while allowing for different project scales. |
| **Authoring** | **Medium** | Must contain Context, Decision, and Consequences. | Choice of template (MADR, Nygard, Y-Statement) is left to the team. | Guarantees utility for the reader while respecting developer preference for tools. |
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
1.  Use `adr-authoring` to select the appropriate template.
2.  Draft the ADR, ensuring the **Consequences** section is honest and detailed (including the downsides).
3.  Submit the ADR for review as part of the technical design approval.

### Step 3: The Maintenance Loop (`adr-lifecycle-management`)
Once the decision is live and the project evolves:
1.  **New Decision?** Create a new ADR and use the lifecycle skill to update the index.
2.  **Superseding a Decision?** Use the lifecycle skill to create the bidirectional link between the old and new records.
3.  **Retiring a Decision?** Mark as `Deprecated` or `Superseded`; never delete the file.

## 5. Success Metrics
*   **Traceability**: Can a new engineer find the "why" for a core system component in under 2 minutes?
*   **Consistency**: Do all ADRs follow a recognizable structure?
*   **Integrity**: Are there any "orphaned" decisions (decisions with no links to what superseded them)?
