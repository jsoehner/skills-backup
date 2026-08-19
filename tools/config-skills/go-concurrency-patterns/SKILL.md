---
name: go-concurrency-patterns
description: Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions.
---

# Go Concurrency Patterns

Production patterns for Go concurrency including goroutines, channels, synchronization primitives, and context management.

## Use this skill when

- Building concurrent Go applications
- Implementing worker pools and pipelines
- Managing goroutine lifecycles
- Using channels for communication
- Debugging race conditions
- Implementing graceful shutdown

## Do not use this skill when

- The task is unrelated to go concurrency patterns
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

After a concurrent Go system or complex worker pool pattern is implemented, automatically trigger the `capture_knowledge.py` script.
The script will analyze the concurrency model to identify:
- New worker pool patterns or channel communication flows.
- Complex `sync` primitive usage (WaitGroups, Mutexes, Conds).
- Context-aware cancellation and timeout logic.
The script will then route this information to the appropriate storage:
- **OKF**: High-level concurrency safety rules, worker pool standards, and graceful shutdown policies.
- **ChromaDB**: Specific goroutine implementations, channel-based pipelines, and sync-related logic.
",path: