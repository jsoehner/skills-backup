---
name: code-review-excellence
description: Master effective code review practices to provide constructive feedback, catch bugs early, and foster knowledge sharing while maintaining team morale. Use when reviewing pull requests, establishing review standards, or mentoring developers.
---

# Code Review Excellence

Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement.

## Use this skill when

- Reviewing pull requests and code changes
- Establishing code review standards
- Mentoring developers through review feedback
- Auditing for correctness, security, or performance

## Do not use this skill when

- There are no code changes to review
- The task is a design-only discussion without code
- You need to implement fixes instead of reviewing

## Instructions

- Read context, requirements, and test signals first.
- Review for correctness, security, performance, and maintainability.
- Provide actionable feedback with severity and rationale.
- Ask clarifying questions when intent is unclear.
- If detailed checklists are required, open `resources/implementation-playbook.md`.

## Output Format

- High-level summary of findings
- Issues grouped by severity (blocking, important, minor)
- Suggestions and questions
- Test and coverage notes

## Resources

- `resources/implementation-playbook.md` for detailed review patterns and templates.

## Knowledge Capture Requirement
When performing tasks that involve architectural decisions, significant engineering trade-offs, or complex infrastructure changes, you MUST use the `capture_knowledge.py` script to persist the information.

- **Policy/High-Level Decisions**: Use `python3 capture_knowledge.py --type okf` to save to the Open Knowledge Framework (OKF).
- **Technical Context/Implementation Details**: Use `python3 capture_knowledge.py --type chroma` to save to the contextual memory (ChromaDB).

Ensure that the captured content is deduplicated (the script handles this via hashing) and correctly chunked.

## Anti-Patterns