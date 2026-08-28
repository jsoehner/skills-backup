---
name: adr-authoring
description: "Guide the selection of ADR templates (e.g., MADR, Nygard, Y-Statement) and author high-quality Architectural Decision Records that focus on context, rationale, and consequences. Trigger when requested to draft, write, or format a new ADR. Keywords: MADR, Nygard, Y-statement, architectural rationale, trade-offs, consequences."
---

# ADR Authoring - Drafting Decisions with Rationale

This skill helps the agent and team author high-quality Architectural Decision Records (ADRs) using industry-standard templates and structures that emphasize context, clear trade-offs, and downstream consequences.

## Progressive Disclosure & External Resources

- **External Resources**: This is a self-contained skill. Templates are described inline. No external scripts are required.
- **Reference**: For more details, refer to the templates list at [adr.github.io/adr-templates/](https://adr.github.io/adr-templates/).

## Freedom Calibration & Constraints

- **Constraint Level: Medium**
  - **High Rigidity**: All drafted ADRs must contain the three fundamental sections: Context, Decision (with status), and Consequences (trade-offs, new risks, required updates).
  - **High Freedom**: The selection of template format (e.g., Nygard vs. MADR vs. Y-Statement) is left to team preference or project conventions.

## Decision Tree: Choosing the Right Template

```
Determine Target Audience & Depth
 ├─ Lightweight, developer-focused, markdown-native → [Use MADR (Markdown ADR) Template]
 ├─ Industry standard, simple, narrative structure → [Use Nygard Template]
 ├─ Formal, enterprise-grade, highly structured, reason-based → [Use Y-Statement Template]
 └─ Agile, brief, minimal overhead → [Use Lightweight Paragraph Template]
```

## Professional Mindset & Design Principles

1. **Consequences over Rationale**: The impact of a decision (what it enables, disables, forces, or limits) is more important than why it was chosen.
2. **Honest Trade-offs**: Every design choice has downsides. Refusing to document negatives in an ADR is an anti-pattern.
3. **No Retrospective Rewriting**: Keep ADRs short, objective, and contemporaneous. Write it when the decision is made.

---

## Step-by-Step Execution Procedure

### Step 1: Choose the ADR Template

Review the decision requirements (assessed in `adr-discovery`) and select one of the following official templates:

#### Option A: Minimum ADR Template
- **Usage**: Low-risk, local, reversible, or component-level architecturally significant decisions.
- **Template File**: `/Users/jsoehner/.gemini/config/skills/adr-templates/Minimum_ADR_Template.md`
- **Key Sections**: Metadata, Context (Problem Statement, Current Situation), Alternatives Considered, Decision, Rationale, Consequences (Positive, Negative, Follow-on), Related Records.

#### Option B: Standard ADR Template (Default)
- **Usage**: Enterprise default for production application, platform, cloud, security, data, infrastructure, and integration decisions.
- **Template File**: `/Users/jsoehner/.gemini/config/skills/adr-templates/Standard_ADR_Template.md`
- **Key Sections**: Metadata, Business and Architecture Context, Assumptions, Constraints, Alternatives Considered (table format), Decision (Selected Option, Rationale), Consequences (Benefits, Trade-offs/Negatives, New Constraints, Follow-on), Security/Risk/Control Impact, Technical Debt Assessment, Traceability, Review and Lifecycle.

#### Option C: Comprehensive ADR Template
- **Usage**: Enterprise-critical, regulated, security-sensitive, cross-domain, strategic-platform, significant third-party, standards-exception, material-risk, or material-technical-debt decisions.
- **Template File**: `/Users/jsoehner/.gemini/config/skills/adr-templates/Comprehensive_ADR_Template.md`
- **Key Sections**: Metadata, Governance Classification, Stakeholders/Accountability, Business and Architecture Context, Assumptions/Constraints, Alternatives Considered (Detailed scoring matrix), Decision, Consequences, Security/Privacy/Risk/Compliance Assessment, Technical Debt Assessment, Third-Party/Supply-Chain Assessment, Implementation/Transition, Operational Readiness, Validation/Conformance, Traceability, Outcome Review, Review/Supersession/Lifecycle, Audit/Records Management, Change Log.

Read the chosen template file directly to get its exact markdown structure and placeholders.

### Step 2: Gather Context and Trade-offs

- Query/discuss the technical drivers (e.g., Performance, Cost, Complexity, Vendor Lock-in).
- List the alternative options that were realistically considered.
- Define the pros and cons of each option.

### Step 3: Write and Review the Record

- Populate the chosen template.
- Ensure the filename follows standard naming patterns: `docs/adr/NNNN-title-in-kebab-case.md` (e.g., `docs/adr/0004-use-postgres-for-caching.md`).
- Validate that the consequences section includes actionable items (e.g., team training, migration scripts, documentation updates).
- Trigger the local memory capture using the standardized capture script.

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** hide negatives | Omitting negative consequences or pretending a solution has no downsides. | Devote an equal effort to documenting negative consequences/trade-offs. |
| **NEVER** write a blog post | Writing long, rambling essays instead of a concise, structured record. | Keep ADRs short (1-2 pages maximum). Use bullet points. |
| **NEVER** lose track of status | Forgetting to mark status, leading to confusion about what is active. | Keep the Status section at the top of the file, clear and updated. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: Lack of Consensus on Trade-offs

- **Root Cause**: Team members disagree on the pros/cons of considered options.
- **Fallback**:
  1. Document all differing opinions honestly in the "Pros and Cons" section.
  2. Let the owner/lead architect make the final decision outcome.
  3. Change status to "Proposed" and open a PR for collective review.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
