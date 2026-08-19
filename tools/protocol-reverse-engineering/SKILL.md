---
name: protocol-reverse-engineering
description: Master network protocol reverse engineering including packet analysis, protocol dissection, and custom protocol documentation. Use when analyzing network traffic, understanding proprietary protocols, or debugging network communication.
---

# Protocol Reverse Engineering

Comprehensive techniques for capturing, analyzing, and documenting network protocols for security research, interoperability, and debugging.

## Use this skill when

- Working on protocol reverse engineering tasks or workflows
- Needing guidance, best practices, or checklists for protocol reverse engineering

## Do not use this skill when

- The task is unrelated to protocol reverse engineering
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.


## 6) Memory Sync

After completing a task, key decision, or report, you **MUST** trigger the local memory capture. 

1. Save the final document, report, or summary as a Markdown file in the project directory.
2. Invoke the capture script: 
   `ash
   python \capture_knowledge.py <file_path>
   `
3. This ensures that new requirements, technical standards, and findings are automatically routed to the correct storage (OKF or ChromaDB).
