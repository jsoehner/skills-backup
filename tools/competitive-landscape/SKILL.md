---
name: competitive-landscape
description: This skill should be used when the user asks to "analyze
  competitors", "assess competitive landscape", "identify differentiation",
  "evaluate market positioning", "apply Porter's Five Forces", or requests
  competitive strategy analysis.
metadata:
  version: 1.0.0
---

# Competitive Landscape Analysis

Comprehensive frameworks for analyzing competition, identifying differentiation opportunities, and developing winning market positioning strategies.

## Use this skill when

- Working on competitive landscape analysis tasks or workflows
- Needing guidance, best practices, or checklists for competitive landscape analysis

## Do not use this skill when

- The task is unrelated to competitive landscape analysis
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
