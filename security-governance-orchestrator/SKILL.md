---
name: "security-governance-orchestrator"
description: "Orchestrates security governance, including audits, compliance, threat modeling, and vulnerability scanning."
version: 1
created: "2026-07-31"
updated: "2026-07-31"
metadata:
  model: inherit
dependencies:
  - security-auditor
  - security-compliance-compliance-check
  - threat-modeling-expert
  - stride-analysis-patterns
  - security-scanning-security-dependencies
  - security-scanning-security-hardening
  - security-scanning-security-sast
  - security-requirement-extraction
---
## When to Use
Use for any task involving security auditing, compliance, threat modeling, or vulnerability scanning.

## Procedure
1. Identify the security task: Audit, Compliance, Threat Modeling, or Vulnerability Scanning.
2. For Security Audits: Use `security-auditor` and `security-compliance-compliance-check` to evaluate the codebase and compliance posture.
3. For Threat Modeling: Use `threat-modeling-expert` and `stride-analysis-patterns` to identify potential attack vectors.
4. For Vulnerability Scanning: Use `security-scanning-security-dependencies`, `security-scanning-security-hardening`, and `security-scanning-security-sast`.
5. For Requirement Extraction: Use `security-requirement-extraction`.
6. Synthesize the security posture into a comprehensive report with actionable remediation steps.

## Pitfalls
- Never skip a security audit for production-ready code.
- Ensure threat models are updated as the architecture evolves.
- Do not ignore compliance requirements (GDPR, HIPAA, etc.).

## Verification
1. Security audit report is comprehensive and accurate.
2. Threat model accurately reflects the current architecture.
3. Vulnerability scan results are reviewed and acted upon.