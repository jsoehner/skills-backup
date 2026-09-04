---
name: startup-metrics-framework
description: This skill should be used when the user asks about "key startup
  metrics", "SaaS metrics", "CAC and LTV", "unit economics", "burn multiple",
  "rule of 40", "marketplace metrics", or requests guidance on tracking and
  optimizing business performance metrics.
metadata:
  version: 1.0.0
---

# Startup Metrics Framework

Comprehensive guide to tracking, calculating, and optimizing key performance metrics for different startup business models from seed through Series A.

## Use this skill when

- Working on startup metrics framework tasks or workflows
- Needing guidance, best practices, or checklists for startup metrics framework

## Do not use this skill when

- The task is unrelated to startup metrics framework
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

## 6) Capture Knowledge


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
