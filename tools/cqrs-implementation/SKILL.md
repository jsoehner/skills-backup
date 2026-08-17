---
name: cqrs-implementation
description: Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems.
---

# CQRS Implementation

Comprehensive guide to implementing CQRS (Command Query Responsibility Segregation) patterns.

## Use this skill when

- Separating read and write concerns
- Scaling reads independently from writes
- Building event-sourced systems
- Optimizing complex query scenarios
- Different read/write data models are needed
- High-performance reporting is required

## Do not use this skill when

- The domain is simple and CRUD is sufficient
- You cannot operate separate read/write models
- Strong immediate consistency is required everywhere

## Instructions

- Identify read/write workloads and consistency needs.
- Define command and query models with clear boundaries.
- Implement read model projections and synchronization.
- Validate performance, recovery, and failure modes.
- If detailed patterns are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed CQRS patterns and templates.

## Knowledge Capture Requirement
When performing tasks that involve architectural decisions, significant engineering trade-offs, or complex infrastructure changes, you MUST use the `capture_knowledge.py` script to persist the information.

- **Policy/High-Level Decisions**: Use `python3 capture_knowledge.py --type okf` to save to the Open Knowledge Framework (OKF).
- **Technical Context/Implementation Details**: Use `python3 capture_knowledge.py --type chroma` to save to the contextual memory (ChromaDB).

Ensure that the captured content is deduplicated (the script handles this via hashing) and correctly chunked.


- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.
