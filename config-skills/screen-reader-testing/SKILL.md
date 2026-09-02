---
name: screen-reader-testing
description: Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging accessibility issues, or ensuring assistive technology support.
---

# Screen Reader Testing

Practical guide to testing web applications with screen readers for comprehensive accessibility validation.

## Use this skill when

- Validating screen reader compatibility
- Testing ARIA implementations
- Debugging assistive technology issues
- Verifying form accessibility
- Testing dynamic content announcements
- Ensuring navigation accessibility

## Do not use this skill when

- The task is unrelated to screen reader testing
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.
- Trigger the `capture_knowledge.py` script to record screen reader compatibility findings, ARIA bug reports, and accessibility remediation strategies.

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
