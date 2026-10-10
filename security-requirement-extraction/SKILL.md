---
name: security-requirement-extraction
description: Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases.
---

# Security Requirement Extraction

Transform threat analysis into actionable security requirements.

## Use this skill when

- Converting threat models to requirements
- Writing security user stories
- Creating security test cases
- Building security acceptance criteria
- Compliance requirement mapping
- Security architecture documentation

## Do not use this skill when

- The task is unrelated to security requirement extraction
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- Trigger the `capture_knowledge.py` script to record security requirements, user stories, and test case specifications.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER leak credentials, private keys, or API tokens in code repositories or application logs.
- NEVER trust client-side inputs without performing strict server-side validation.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
