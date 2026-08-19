---
name: threat-mitigation-mapping
description: Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness.
---

# Threat Mitigation Mapping

Connect threats to controls for effective security planning.

## Use this skill when

- Prioritizing security investments
- Creating remediation roadmaps
- Validating control coverage
- Designing defense-in-depth
- Security architecture review
- Risk treatment planning

## Do not use this skill when

- The task is unrelated to threat mitigation mapping
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER leak credentials, private keys, or API tokens in code repositories or application logs.
- NEVER trust client-side inputs without performing strict server-side validation.


## 6) Memory Sync

After completing a task, key decision, or report, you **MUST** trigger the local memory capture. 

1. Save the final document, report, or summary as a Markdown file in the project directory.
2. Invoke the capture script: 
   `ash
   python \capture_knowledge.py <file_path>
   `
3. This ensures that new requirements, technical standards, and findings are automatically routed to the correct storage (OKF or ChromaDB).
