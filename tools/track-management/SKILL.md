---
name: track-management
description: Use this skill when creating, managing, or working with Conductor
  tracks - the logical work units for features, bugs, and refactors. Applies to
  spec.md, plan.md, and track lifecycle operations.
metadata:
  version: 1.0.0
---

# Track Management

Guide for creating, managing, and completing Conductor tracks - the logical work units that organize features, bugs, and refactors through specification, planning, and implementation phases.

## Use this skill when

- Creating new feature, bug, or refactor tracks
- Writing or reviewing spec.md files
- Creating or updating plan.md files
- Managing track lifecycle from creation to completion
- Understanding track status markers and conventions
- Working with the tracks.md registry
- Interpreting or updating track metadata

## Do not use this skill when

- The task is unrelated to track management
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

## Knowledge Capture Requirement

After completing a significant architectural decision, security policy update, or complex bug fix, you **must** capture this knowledge. 
1. Synthesize the decision/fix into a concise summary.
2. Run `capture_knowledge.py` (or the orchestrator) to persist this to the project's knowledge base.
3. Confirm the save to the user.
