---
name: error-handling-patterns
description: Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build resilient applications. Use when implementing error handling, designing APIs, or improving application reliability.
---

# Error Handling Patterns

Build resilient applications with robust error handling strategies that gracefully handle failures and provide excellent debugging experiences.

## Use this skill when

- Implementing error handling in new features
- Designing error-resilient APIs
- Debugging production issues
- Improving application reliability
- Creating better error messages for users and developers
- Implementing retry and circuit breaker patterns
- Handling async/concurrent errors
- Building fault-tolerant distributed systems

## Do not use this skill when

- The task is unrelated to error handling patterns
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

Execute the following steps to sync knowledge to the memory system:
1. Use `capture_knowledge.py` to route information to the correct storage (OKF or ChromaDB).
2. Ensure that high-level architectural rules, policies, and decisions are stored in the OKF (Open Knowledge Format) directory.
3. Ensure that ephemeral data, logs, and specific technical notes are stored in the ChromaDB instance.
4. Verify that the `MEMORY_SYSTEM_ROOT` and `MEMORY_INBOX_DIR` environment variables are correctly configured.
