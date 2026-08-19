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
