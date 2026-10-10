# [SecADR-XXXX]: [Short Title of Security Decision]

- **Status**: [Proposed | Accepted | Superseded by [SecADR-YYYY](file:///docs/adr/YYYY-title.md) | Deprecated]
- **Date**: YYYY-MM-DD
- **Security Classification**: [Public | Internal | Confidential | Restricted]
- **Decision Makers**: [Name/Role, e.g., Jane Doe (SecOps Lead), John Smith (AppSec Eng)]
- **Consulted / Informed**: [e.g., Platform Team, Compliance, Engineering Leads]
- **Supersedes**: [None | [SecADR-ZZZZ](file:///docs/adr/ZZZZ-old-decision.md)]

---

## 1. Context and Problem Statement

[Describe the security context, vulnerability, compliance mandate, or architectural change prompting this decision. What problem are we solving? What is the current threat or risk?]

### 1.1 Business & Compliance Drivers
- **Regulatory / Compliance**: [e.g., SOC2 CC6.1, ISO 27001 A.9.4.2, PCI-DSS 3.4, HIPAA §164.312, GDPR Art. 32]
- **Business Need**: [e.g., Customer requirement for SSO, data sovereignty, protection of PII]

### 1.2 Threat & Vulnerability Context
- **Threat Vector (STRIDE)**: [Spoofing | Tampering | Repudiation | Information Disclosure | Denial of Service | Elevation of Privilege]
- **Vulnerability / CVE Reference**: [e.g., CVE-2026-XXXX, CWE-287, or Internal Penetration Test Finding #14]
- **CVSS / Risk Rating**: [Critical | High | Medium | Low] (Score: X.X)
- **Affected Assets & Boundaries**: [e.g., User Authentication Token Store, Payment Processing Ingress, API Gateway]

---

## 2. Decision Drivers & Constraints

- [Driver 1: Zero-trust network boundary between edge services and data tier]
- [Driver 2: Enforce cryptographic standards: AES-256-GCM / TLS 1.3]
- [Constraint 1: Must avoid breaking changes for existing v1 mobile client apps]
- [Constraint 2: Cloud KMS API latency budget must remain < 15ms]

---

## 3. Considered Options

| Option | Approach Summary | Security Benefits | Trade-offs & Costs | Residual Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| **Option A (Chosen)** | [e.g., OIDC with JWT short-lived tokens & refresh rotation] | Eliminates long-lived session hijacking, standard-based | Requires Redis token-revocation denylist, minor latency | Low |
| **Option B** | [e.g., Server-side sessions in PostgreSQL] | Immediate global revocation capability | Database scaling bottleneck under high load | Medium |
| **Option C** | [e.g., Third-party Identity Provider (Auth0/Okta)] | Zero custom crypto code, out-of-the-box compliance | High licensing cost, vendor lock-in | Low |

---

## 4. Decision Outcome

**Chosen Option**: **Option A** — [Name of Selected Option]

### 4.1 Rationale
[Explain why this option best addresses the problem statement, drivers, and constraints. Detail how it satisfies the required security controls while balancing usability and performance.]

### 4.2 Architectural Changes & Flow
[Describe architectural modifications, protocol changes, trust boundary alterations, or cipher suites adopted.]

```
[Client] ──(HTTPS/TLS 1.3)──> [API Gateway] ──(mTLS / JWT Validation)──> [Internal Microservices]
                                    │
                         (Validate Signature / Revocation)
                                    ▼
                         [Distributed Cache (Redis)]
```

---

## 5. Security, Risk & Compliance Impact

### 5.1 CIA Triad Evaluation
- **Confidentiality**: [How is data protected from unauthorized disclosure?]
- **Integrity**: [How are tampering and replay attacks mitigated?]
- **Availability**: [What is the DoS resilience, rate-limiting, or failover strategy?]

### 5.2 Residual Risk & Compensating Controls
- **Residual Risk**: [State any remaining accepted risk explicitly. No security choice has zero residual risk.]
- **Compensating Controls**: [e.g., WAF rate limiting, anomaly detection alerts, audit logging in CloudTrail/Stackdriver]

### 5.3 Compliance Traceability
- **Control Satisfied**: [e.g., NIST SP 800-63B Authenticator Assurance Level 2]
- **Audit Evidence Artifact**: [e.g., Access logs retained in cold storage for 365 days with SHA-256 checksums]

---

## 6. Consequences & Downstream Impact

### 6.1 Positive Consequences
- [e.g., Mitigates credential replay attacks across distributed cluster]
- [e.g., Simplifies third-party SOC2 Type II audit trail]

### 6.2 Negative Consequences & Technical Debt
- [e.g., Introduces operational dependency on Redis cluster availability]
- [e.g., Developers must update local dev environment docker-compose setup]

### 6.3 Follow-On Tasks
- [ ] [Create GitHub issue to migrate v1 authentication endpoints]
- [ ] [Update `.github/workflows/security-governance.yml` with Semgrep rule checking for deprecated auth calls]
- [ ] [Update developer documentation in `docs/security/authentication.md`]

---

## 7. Verification & Conformance

- **Automated Verification**: [e.g., Automated integration test suite `npm run test:security` validates token expiry and signature rejection]
- **Static Analysis / Linter Rule**: [e.g., Semgrep rule `rules/auth-no-raw-tokens.yml` configured in CI to block raw token usage]
- **Review Schedule**: [Annual review or upon major cryptographic standard changes]

---

## 8. Record Lifecycle & History

| Date | Author | Status Change | Summary |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | [Author Name] | Proposed | Initial draft following threat model review |
| YYYY-MM-DD | [Security Lead] | Accepted | Approved by Architecture Review Board |
