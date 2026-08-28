# Comprehensive Architecture Decision Record Template

> **Template type:** Comprehensive ADR  
> **Intended use:** Enterprise-critical, regulated, security-sensitive, cross-domain, strategic-platform, significant third-party, standards-exception, material-risk, or material-technical-debt decisions.  
> **Completion guidance:** This template incorporates the Standard ADR fields and adds full governance, assurance, implementation, operational, and records-management detail. Replace all `{placeholders}` and use stable identifiers for external records.

# ADR-{ID}: {Decision Title}

## Metadata

| Field | Value |
|---|---|
| ADR ID | ADR-{ID} |
| Status | Draft / Proposed / Under Review / Accepted / Accepted with Conditions / Rejected / Implemented / Validated / Deprecated / Superseded / Retired / Archived |
| Created Date | YYYY-MM-DD |
| Decision Date | YYYY-MM-DD |
| Effective Date | YYYY-MM-DD |
| Architecture Domain(s) | Business / Data / Application / Technology / Security / Integration / Infrastructure / Resilience / Enterprise |
| Scope | {System, service, platform, capability, programme, or enterprise domain} |
| Decision Owner | {Durable accountable role} |
| Named Decision Maker | {Name and role at time of decision} |
| Approval Authority | {Role, ARB, committee, or delegated forum} |
| Approval Evidence ID | {Approval record or meeting decision ID} |
| APM Code(s) | {None or APM ID list} |
| NIRA Reference(s) | {None or NIRA ID list} |
| Repository Location | {Canonical record location} |
| Tags | {Searchable domain and governance tags} |

---

## Governance Classification

| Field | Value |
|---|---|
| Decision Classification | Strategic / Tactical / Operational |
| Decision Significance / Risk Tier | Critical / High / Medium / Low or Enterprise Tier |
| Decision Horizon | Temporary / Transitional / Medium-Term / Long-Term / Permanent |
| Reversibility | Easy / Moderate / Difficult / Nearly Irreversible |
| Business Criticality | Tier 0 / Tier 1 / Tier 2 / Tier 3 / Not Applicable |
| Data Classification | Public / Internal / Confidential / Restricted / Other |
| Regulatory Scope | {Regulations, obligations, or None} |
| Jurisdictions | {Countries, regions, or None} |
| Record Classification | {Records and information classification} |

---

## Stakeholders, Accountability, and Decision Proceedings

| Responsibility | Name / Role / Forum |
|---|---|
| ADR Author / Proposer | {Name and role} |
| Decision Owner | {Accountable role and named role holder} |
| Business Owner | {Name and role} |
| Technology Owner | {Name and role} |
| Product / Service Owner | {Name and role} |
| Security Owner / Reviewer | {Name and role} |
| Operations / SRE Owner | {Name and role} |
| Risk Representative | {Name and role} |
| Compliance / Privacy Representative | {Name and role} |
| Architecture Review Authority | {Forum and decision ID} |
| Risk Acceptor, if applicable | {Name, role, and delegated authority} |
| Informed Stakeholders | {Teams or roles} |

### Dissenting Opinions and Unresolved Concerns

{Capture material objections, unresolved concerns, minority opinions, and how each was addressed or accepted.}

### Approval Conditions

| Condition | Owner | Due Date | Evidence / Status |
|---|---|---|---|
| {Condition} | {Role} | YYYY-MM-DD | {ID or status} |

---

## Business and Architecture Context

### Executive Summary

{Summarize the decision, why it matters, and the selected direction in two to four concise sentences.}

### Problem Statement

{Describe the architecturally significant question, problem, opportunity, or requirement being resolved.}

### Current Situation

{Describe the current architecture, business context, risk posture, dependencies, limitations, and urgency.}

### Decision Drivers

- **Business:** {Driver}
- **Customer:** {Driver}
- **Technical:** {Driver}
- **Security:** {Driver}
- **Privacy / Data:** {Driver}
- **Regulatory / Compliance:** {Driver}
- **Resilience / Availability:** {Driver}
- **Operational:** {Driver}
- **Cost / Schedule:** {Driver}
- **Strategic Alignment:** {Driver}

---

## Assumptions and Constraints

### Assumptions

| Assumption | Evidence | Invalidation Trigger |
|---|---|---|
| {Assumption} | {Reference} | {Event requiring review} |

### Constraints

| Constraint | Source | Effect on Decision |
|---|---|---|
| {Constraint} | {Policy, standard, contract, deadline, skill, cost, or technology source} | {Impact} |

---

## Alternatives Considered

### Option Summaries

| Option | Description | Disposition |
|---|---|---|
| {Option A} | {Summary} | Selected / Rejected |
| {Option B} | {Summary} | Selected / Rejected |
| Status quo / Do nothing | {Summary} | Selected / Rejected / Not viable |

### Detailed Option Evaluation

Define weights and scoring scales before scoring the options.

| Evaluation Criterion | Weight | Option A | Option B | Status Quo | Evidence / Notes |
|---|---:|---:|---:|---:|---|
| Security | {%} | {Score} | {Score} | {Score} | {Reference} |
| Privacy / Data Protection | {%} | {Score} | {Score} | {Score} | {Reference} |
| Resilience / Availability | {%} | {Score} | {Score} | {Score} | {Reference} |
| Operability | {%} | {Score} | {Score} | {Score} | {Reference} |
| Cost / Total Cost of Ownership | {%} | {Score} | {Score} | {Score} | {Reference} |
| Strategic Alignment | {%} | {Score} | {Score} | {Score} | {Reference} |
| Vendor / Concentration Risk | {%} | {Score} | {Score} | {Score} | {Reference} |
| Complexity / Skills | {%} | {Score} | {Score} | {Score} | {Reference} |
| Reversibility / Exit | {%} | {Score} | {Score} | {Score} | {Reference} |

---

## Decision

### Selected Option

{State the decision clearly and affirmatively.}

### Rationale

{Explain why this option was selected based on the drivers, evaluation evidence, trade-offs, and stakeholder challenge.}

### Confidence and Evidence Quality

| Field | Value |
|---|---|
| Decision Confidence | High / Medium / Low |
| Evidence Quality | Strong / Moderate / Limited |
| Key Evidence Gaps | {None or gaps} |

---

## Consequences

### Positive Consequences

- {Benefit or desired outcome}

### Negative Consequences and Accepted Trade-offs

- {Risk, cost, limitation, lock-in, complexity, or operational burden}

### New Constraints

- {Constraint created by the decision}

### Follow-on Decisions and Activities

- {Subsequent ADR, remediation item, implementation action, or governance obligation}

---

## Security, Privacy, Risk, and Compliance Assessment

### Threat Scenarios

| Threat / Abuse Case | Affected Asset or Trust Boundary | Likelihood | Impact | Treatment / Reference |
|---|---|---|---|---|
| {Threat} | {Asset or boundary} | {Rating} | {Rating} | {Control or assessment ID} |

### Security Requirements and Controls

| Requirement / Control ID | Description | Decision Impact | Implementation Evidence |
|---|---|---|---|
| {ID} | {Requirement or control} | Implements / Modifies / Depends on / Deviates | {Reference} |

### Privacy and Data Impact

| Area | Impact / Decision |
|---|---|
| Personal Information | {None or impact} |
| Data Classification | {Classification and treatment} |
| Data Residency | {Locations and constraints} |
| Cross-Border Data Movement | {None or details} |
| Data Sharing / Third Parties | {None or details} |
| Retention / Disposal | {Requirements} |
| Consent / Permitted Use | {None or requirements} |

### Resilience Impact

| Area | Requirement / Impact |
|---|---|
| Availability | {Target and impact} |
| Recovery Time Objective | {RTO} |
| Recovery Point Objective | {RPO} |
| Disaster Recovery | {Decision and evidence} |
| Capacity / Scalability | {Target and impact} |
| Critical Dependencies | {List or reference} |

### Regulatory and Standards Alignment

| Regulation / Policy / Standard / Pattern | Relationship | Evidence or Exception ID |
|---|---|---|
| {Reference} | Aligns / Partially aligns / Deviates / Not applicable | {Reference} |

### Residual Risk, Exceptions, and Compensating Controls

| Risk / Exception ID | Residual Risk | Compensating Control ID(s) | Risk Owner | Expiry / Review |
|---|---|---|---|---|
| {ID} | {Rating and summary} | {IDs} | {Role} | YYYY-MM-DD |

### Risk Acceptance

| Field | Value |
|---|---|
| Risk Acceptance Required | Yes / No |
| Risk Acceptance ID | {None or ID} |
| Named Risk Acceptor | {Name and role} |
| Delegated Authority Basis | {Reference} |
| Acceptance Date | YYYY-MM-DD |

---

## Technical Debt Assessment

### Debt Impact

Select one or more relationships:

- [ ] No technical debt impact
- [ ] Introduces technical debt
- [ ] Continues existing technical debt
- [ ] Retires technical debt

### Technical Debt References

| Debt ID | Relationship | Affected Component | Brief Decision Context |
|---|---|---|---|
| {TD-ID} | Introduces / Continues / Retires | {Asset ID} | {Why this debt is related to the decision} |

> The technical-debt registry is authoritative for debt type, risk drivers, ownership, priority, compensating controls, remediation plan, target date, status, and closure evidence. The ADR preserves the immutable decision context and typed relationship.

---

## Third-Party and Supply-Chain Assessment

| Third Party / Dependency | Service or Capability | Data / Control Role | Risk Assessment ID | Contract / Exit Impact |
|---|---|---|---|---|
| {Vendor or component} | {Capability} | {Role} | {ID} | {Summary} |

### Concentration and Dependency Risk

{Describe concentration, proprietary dependency, subprocessor, open-source, service continuity, and control-responsibility considerations.}

### Exit Strategy

{Describe portability, data return/destruction, migration, replacement, contract termination, and operational exit criteria.}

---

## Implementation and Transition

### Affected Assets

| Asset Type | Identifier / Name | Impact |
|---|---|---|
| Application / APM Record | {ID} | {Impact} |
| Service / Platform | {ID or name} | {Impact} |
| Component / Interface | {ID or name} | {Impact} |
| Business Capability | {ID or name} | {Impact} |

### Dependencies and Prerequisites

- {Dependency or prerequisite}

### Migration Plan

- {Migration stage, owner, milestone, and exit criterion}

### Transition Architecture

{Describe temporary coexistence, interim controls, dual-running, and transition-state dependencies.}

### Rollback and Contingency Plan

{Describe rollback criteria, recovery approach, data reconciliation, decision authority, and contingency controls.}

---

## Operational Readiness

| Area | Requirement / Reference |
|---|---|
| Support Model | {Owner and support model} |
| Monitoring | {Metrics, dashboards, and ownership} |
| Security Logging | {Events, destination, retention, and access} |
| Alerting | {Thresholds and response ownership} |
| Incident Response | {Playbook or runbook ID} |
| Problem Management | {Process / ownership} |
| Backup and Recovery | {Requirement and test evidence} |
| Capacity Management | {Thresholds and ownership} |
| Service Management | {Service record or operational acceptance ID} |

### Runbooks and Procedures

| Artifact Type | Reference |
|---|---|
| Operational Runbook | {ID or link} |
| Security Playbook | {ID or link} |
| Standard Operating Procedure | {ID or link} |
| Disaster Recovery Plan | {ID or link} |

---

## Validation and Conformance

### Architecture Fitness Functions and Success Criteria

| Measure / Rule | Target | Validation Method | Owner | Evidence |
|---|---|---|---|---|
| {Metric, policy, or architecture rule} | {Target} | Automated / Manual | {Role} | {Reference} |

### Validation Activities

- [ ] Architecture conformance review
- [ ] Threat model review
- [ ] Security testing
- [ ] Privacy / data review
- [ ] Resilience / disaster-recovery testing
- [ ] Performance and capacity testing
- [ ] Operational-readiness review
- [ ] Control-effectiveness validation

### Validation Evidence

| Evidence Type | Reference | Date | Result |
|---|---|---|---|
| {Test, review, scan, attestation, or certification} | {ID} | YYYY-MM-DD | Passed / Conditional / Failed |

---

## Traceability

| Relationship Type | Reference | Relationship |
|---|---|---|
| Requirement | {REQ-ID} | Satisfies / Constrains / Derived from |
| Business Capability | {Capability ID} | Enables / Changes / Supports |
| Risk | {RISK-ID} | Creates / Mitigates / Accepts |
| Control | {CTRL-ID} | Implements / Modifies / Depends on |
| Standard / Pattern | {ID} | Aligns / Partially aligns / Deviates |
| Reference Architecture | {ID} | Aligns / Extends / Deviates |
| Project / Programme | {ID} | Funds / Delivers |
| Epic / Work Item | {ID} | Implements / Validates / Remediates |
| Technical Debt | {TD-ID} | Introduces / Continues / Retires |
| ADR | {ADR-ID} | Related / Depends on / Supersedes / Superseded by |
| Change / Release | {ID} | Implements / Validates |
| Incident / Problem / Finding | {ID} | Triggered by / Addresses / Learned from |

---

## Outcome Review

### Expected Outcomes

{Describe expected business, architecture, security, operational, and risk outcomes.}

### Success Measures

| Metric | Baseline | Target | Measurement Date | Owner |
|---|---:|---:|---|---|
| {Metric} | {Baseline} | {Target} | YYYY-MM-DD | {Role} |

### Actual Results

{Complete after implementation or at the scheduled outcome review.}

### Lessons Learned

{Capture observed benefits, unintended consequences, evidence gaps, and recommendations for future decisions.}

---

## Review, Supersession, and Lifecycle

### Review Triggers

- Material change to business, requirements, architecture, risk, or scope
- New or changed regulation, policy, standard, reference architecture, or pattern
- Significant security incident, control failure, audit finding, or threat-model change
- Technology obsolescence, vendor change, contract event, or end of support
- Technical-debt, exception, or risk-acceptance milestone
- Failure to meet an outcome, fitness function, or operational target
- Evidence invalidating an assumption or decision driver

### Lifecycle Information

| Field | Value |
|---|---|
| Planned Review Date | YYYY-MM-DD or Trigger-Based |
| Implemented Date | YYYY-MM-DD or Not Implemented |
| Validated Date | YYYY-MM-DD or Not Validated |
| Supersedes | {None or ADR ID list} |
| Superseded By | {None or ADR ID} |
| Deprecation Date | {None or date} |
| Retirement Date | {None or date} |
| Archive Date | {None or date} |

---

## Audit and Records Management

| Field | Value |
|---|---|
| Record Classification | {Classification} |
| Retention Category / Period | {Schedule reference} |
| Canonical Repository Location | {Location} |
| Approval Evidence Location | {Location or ID} |
| Audit Evidence Package | {Location or ID} |
| Legal Hold | Yes / No / Not Applicable |
| Access Restrictions | {None or restrictions} |

---

## Change Log

| Version | Date | Author | Change | Approval / PR Reference |
|---|---|---|---|---|
| 0.1 | YYYY-MM-DD | {Name} | Initial draft | {Reference} |
