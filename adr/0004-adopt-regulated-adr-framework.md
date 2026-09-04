# ADR-0004: Adopt Regulated Architecture Decision Record (RADR) Framework

## Status

Accepted

## Context

Our teams and clients build software across both general enterprise domains and highly regulated industries (Healthcare/FDA/GxP, Financial Services/PCI-DSS/DORA, ISO 27001, SOC 2, and IEC 62304). While lightweight ADR formats (such as Nygard or MADR) are effective for internal developer velocity, they lack the formal audit envelope, regulatory control traceability, multi-disciplinary sign-off matrices, hazard mitigation mappings, and QMS evidence linkages required by regulatory compliance auditors.

We need our `architecture-decision-records` skill to support both lightweight developer-focused decision records and formal, audit-ready Regulated ADRs (RADRs) aligned with ISO/IEC/IEEE 42010 standards.

## Decision

We will update the `architecture-decision-records` skill to incorporate the **Regulated Architecture Decision Record (RADR)** framework alongside existing lightweight templates. 

Specifically:
1. Add explicit guidelines for when to select standard vs. regulated ADR formats.
2. Define a mandatory 10-part RADR section architecture and metadata schema (Audit Envelope).
3. Integrate ISO/IEC/IEEE 42010 architectural viewpoint alignment, threat/hazard risk mitigation mapping, regulatory clause traceability, and QMS/CI-CD audit evidence strategies.
4. Provide a full production-ready RADR Markdown template.

## Rationale

- **Compliance Assurance**: Provides clear, defensible evidence for auditors without abandoning docs-as-code practices.
- **Traceability**: Enforces a non-repudiable link between regulatory clauses, system requirements, architectural choices, and test validation protocols.
- **Flexibility**: Enables teams to use lightweight MADR/Nygard templates for low-risk changes while leveraging RADR for safety-critical, security-sensitive, or compliance-governed decisions.
- **Standardization**: Aligns organizational software architecture documentation with ISO/IEC/IEEE 42010 and ISO 27001 / IEC 62304 quality management expectations.

## Consequences

### Positive
- Teams in regulated environments can generate audit-ready architectural artifacts directly within Git repositories.
- Reduced time spent translating engineering decisions into formal QMS/GRC compliance dossiers.
- Clearer visibility into security, privacy, and safety trade-offs during architectural reviews.

### Negative
- Increased documentation overhead for compliance-scoped decisions (mitigated by automated CI/CD linter validation).

## Related ADRs
- ADR-0001: Use PostgreSQL as Primary Database
- ADR-0002: Caching Strategy (Redis)
- ADR-0003: Local Memory Management (LanceDB)
