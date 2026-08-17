---
name: code-refactoring-refactor-clean
description: "You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance."
---

# Refactor and Clean Code

You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance.

## Use this skill when

- Refactoring tangled or hard-to-maintain code
- Reducing duplication, complexity, or code smells
- Improving testability and design consistency
- Preparing modules for new features safely

## Do not use this skill when

- You only need a small one-line fix
- Refactoring is prohibited due to change freeze
- The request is for documentation only

## Context
The user needs help refactoring code to make it cleaner, more maintainable, and aligned with best practices. Focus on practical improvements that enhance code quality without over-engineering.

## Requirements
$ARGUMENTS

## Instructions

- Assess code smells, dependencies, and risky hotspots.
- Propose a refactor plan with incremental steps.
- Apply changes in small slices and keep behavior stable.
- Update tests and verify regressions.
- If detailed patterns are required, open `resources/implementation-playbook.md`.

## Safety

- Avoid changing external behavior without explicit approval.
- Keep diffs reviewable and ensure tests pass.

## Output Format

- Summary of issues and target areas
- Refactor plan with ordered steps
- Proposed changes and expected impact
- Test/verification notes

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Knowledge Capture Requirement
When performing tasks that involve architectural decisions, significant engineering trade-offs, or complex infrastructure changes, you MUST use the `capture_knowledge.py` script to persist the information.

- **Policy/High-Level Decisions**: Use `python3 capture_knowledge.py --type okf` to save to the Open Knowledge Framework (OKF).
- **Technical Context/Implementation Details**: Use `python3 capture_knowledge.py --type chroma` to save to the contextual memory (ChromaDB).

Ensure that the captured content is deduplicated (the script handles this via hashing) and correctly chunked.

## Anti-Patterns