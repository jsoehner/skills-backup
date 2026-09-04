---
name: debugging-strategies
description: Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track down bugs across any codebase or technology stack. Use when investigating bugs, performance issues, or unexpected behavior.
---

# Debugging Strategies

Transform debugging from frustrating guesswork into systematic problem-solving with proven strategies, powerful tools, and methodical approaches.

## Use this skill when

- Tracking down elusive bugs
- Investigating performance issues
- Debugging production incidents
- Analyzing crash dumps or stack traces
- Debugging distributed systems

## Do not use this skill when

- There is no reproducible issue or observable symptom
- The task is purely feature development
- You cannot access logs, traces, or runtime signals

## Instructions

- Reproduce the issue and capture logs, traces, and environment details.
- Form hypotheses and design controlled experiments.
- Narrow scope with binary search and targeted instrumentation.
- Document findings and verify the fix.
- If detailed playbooks are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed debugging patterns and checklists.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
