---
name: "security-governance-orchestrator"
description: "Orchestrates security governance, including audits, compliance, threat modeling, and vulnerability scanning."
version: 1
created: "2026-07-31"
updated: "2026-07-31"
---
## When to Use
Use for any task involving security auditing, compliance, threat modeling, or vulnerability scanning.

## Procedure
1. Identify the security task: Audit, Compliance, Threat Modeling, or Vulnerability Scanning.
2. For Security Audits: Use `security-auditor` and `security-compliance-compliance-check` to evaluate the codebase and compliance posture.
3. For Threat Modeling: Use `threat-modeling-expert` and `stride-analysis-patterns` to identify potential attack vectors.
4. For Vulnerability Scanning: Use `security-scanning-security-dependencies`, `security-scanning-security-hardening`, and `security-scanning-security-sast`.
5. For Requirement Extraction: Use `security-requirement-extraction`.
6. Trigger the `capture_knowledge.py` script to record high-level security governance decisions, compliance findings, and threat modeling results.
7. Synthesize the security posture into a comprehensive report with actionable remediation steps.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.

## 6) Capture Knowledge

After a security audit, risk assessment, or threat model is completed, automatically trigger the `capture_knowledge.py` script.
The script will analyze the security findings to identify:
- Key security rules, compliance standards, and risk profiles.
- Critical vulnerabilities, threat vectors, and mitigation strategies.
- Regulatory requirements (GDPR, HIPAA, etc.) and policy-level decisions.
The script will then route this information to the appropriate storage:
- **OKF**: High-level security policies, compliance standards, and corporate security rules.
- **ChromaDB**: Specific audit reports, vulnerability logs, and threat model details.