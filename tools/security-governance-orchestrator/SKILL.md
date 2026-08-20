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


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
