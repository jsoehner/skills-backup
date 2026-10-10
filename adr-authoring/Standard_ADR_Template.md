# Standard Architecture Decision Record Template

> **Template type:** Standard ADR  
> **Intended use:** Enterprise default for production application, platform, cloud, security, data, infrastructure, and integration decisions.  
> **Completion guidance:** Replace all `{placeholders}`. Use stable identifiers and typed references. Authoritative details should remain in their respective registries.

# ADR-{ID}: {Decision Title}

## Metadata

| Field | Value |
|---|---|
| ADR ID | ADR-{ID} |
| Status | Draft / Proposed / Under Review / Accepted / Accepted with Conditions / Rejected / Deprecated / Superseded / Retired |
| Created Date | YYYY-MM-DD |
| Decision Date | YYYY-MM-DD |
| Effective Date | YYYY-MM-DD |
| Architecture Domain | Business / Data / Application / Technology / Security / Integration / Infrastructure / Resilience / Enterprise |
| Scope | {System, service, platform, capability, or domain} |
| Decision Owner | {Durable accountable role} |
| Named Decision Maker | {Name and role at time of decision} |
| Approval Authority | {Role, ARB, committee, or delegated forum} |
| Approval Evidence ID | {Approval record or meeting decision ID} |
| APM Code(s) | {None or APM ID list} |
| NIRA Reference(s) | {None or NIRA ID list} |
| Tags | {Searchable domain tags} |

---

## Business and Architecture Context

### Problem Statement

{Describe the question, problem, opportunity, or architecturally significant requirement being resolved.}

### Current Situation

{Describe the relevant current state and explain why the decision is required now.}

### Decision Drivers

- **Business:** {Driver or None}
- **Technical:** {Driver or None}
- **Security:** {Driver or None}
- **Regulatory:** {Driver or None}
- **Operational:** {Driver or None}
- **Cost / Schedule:** {Driver or None}

---

## Assumptions

- {Assumption that must remain true for the decision to remain valid}

---

## Constraints

- {Technology, policy, schedule, cost, skill, regulatory, or operational constraint}

---

## Alternatives Considered

| Option | Advantages | Disadvantages / Risks | Disposition |
|---|---|---|---|
| {Option 1} | {Benefits} | {Costs, risks, and limitations} | Selected / Rejected |
| {Option 2} | {Benefits} | {Costs, risks, and limitations} | Selected / Rejected |
| Status quo / Do nothing | {Benefits} | {Costs, risks, and limitations} | Selected / Rejected / Not viable |

---

## Decision

### Selected Option

{State the decision clearly and affirmatively.}

### Rationale

{Explain why the selected option best satisfies the decision drivers and why the material alternatives were not selected.}

---

## Consequences

### Benefits

- {Positive consequence}

### Trade-offs and Negative Consequences

- {Accepted downside, risk, cost, or limitation}

### New Constraints

- {Constraint introduced by the decision}

### Follow-on Decisions and Activities

- {Subsequent ADR, implementation obligation, or governance action}

---

## Security, Risk, and Control Impact

| Area | Impact |
|---|---|
| Authentication | {None or impact summary} |
| Authorization | {None or impact summary} |
| Data Protection | {None or impact summary} |
| Logging and Monitoring | {None or impact summary} |
| Privacy | {None or impact summary} |
| Resilience | {None or impact summary} |
| Third-Party / Supply Chain | {None or impact summary} |

### Security and Risk References

| Artifact Type | Reference |
|---|---|
| Threat Model | {None or ID} |
| Threat Risk Assessment | {None or TRA ID} |
| Security Architecture Review | {None or ID} |
| Risk Record | {None or risk ID list} |
| Control Record | {None or control ID list} |
| Exception / Risk Acceptance | {None or ID list} |

---

## Technical Debt Assessment

### Debt Impact

Select one or more relationships:

- [ ] No technical debt impact
- [ ] Introduces technical debt
- [ ] Continues existing technical debt
- [ ] Retires technical debt

### Technical Debt References

| Debt ID | Relationship | Brief Decision Context |
|---|---|---|
| {TD-ID} | Introduces / Continues / Retires | {Why this debt is related to the decision} |

> The technical-debt registry is authoritative for risk, ownership, remediation dates, compensating controls, status, and closure evidence. Do not duplicate mutable debt details in the ADR.

---

## Traceability

### Affected Assets

| Asset Type | Identifier / Name |
|---|---|
| Application / APM Record | {ID} |
| Service / Platform | {ID or name} |
| Component / Interface | {ID or name} |
| Business Capability | {ID or name} |

### Related Records

| Relationship Type | Reference | Relationship |
|---|---|---|
| Requirement | {REQ-ID} | Satisfies / Constrains / Derived from |
| Risk | {RISK-ID} | Creates / Mitigates / Accepts |
| Control | {CTRL-ID} | Implements / Modifies / Depends on |
| Standard / Pattern | {ID} | Aligns / Partially aligns / Deviates |
| Project / Epic / Work Item | {ID} | Implements / Funds / Tracks |
| ADR | {ADR-ID} | Related / Depends on / Supersedes / Superseded by |
| Change / Release | {ID} | Implements / Validates |

---

## Review and Lifecycle

### Review Triggers

- Material change to requirements, risk, architecture, or scope
- New or changed regulation, policy, standard, or pattern
- Significant security incident, control failure, or audit finding
- Technology obsolescence, vendor change, or end of support
- Technical-debt or exception milestone
- New evidence invalidating an assumption or decision driver

### Lifecycle Information

| Field | Value |
|---|---|
| Planned Review Date | YYYY-MM-DD or Trigger-Based |
| Supersedes | {None or ADR ID list} |
| Superseded By | {None or ADR ID} |
| Deprecation / Retirement Notes | {None or summary} |
