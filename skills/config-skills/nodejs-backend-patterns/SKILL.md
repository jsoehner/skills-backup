---
name: nodejs-backend-patterns
description: Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, database integration, and API design best practices. Use when creating Node.js servers, REST APIs, GraphQL backends, or microservices architectures.
---

# Node.js Backend Patterns

Comprehensive guidance for building scalable, maintainable, and production-ready Node.js backend applications with modern frameworks, architectural patterns, and best practices.

## Use this skill when

- Building REST APIs or GraphQL servers
- Creating microservices with Node.js
- Implementing authentication and authorization
- Designing scalable backend architectures
- Setting up middleware and error handling
- Integrating databases (SQL and NoSQL)
- Building real-time applications with WebSockets
- Implementing background job processing

## Do not use this skill when

- The task is unrelated to node.js backend patterns
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


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
