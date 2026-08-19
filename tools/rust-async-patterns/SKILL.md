---
name: rust-async-patterns
description: Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust applications, implementing concurrent systems, or debugging async code.
---

# Rust Async Patterns

Production patterns for async Rust programming with Tokio runtime, including tasks, channels, streams, and error handling.

## Use this skill when

- Building async Rust applications
- Implementing concurrent network services
- Using Tokio for async I/O
- Handling async errors properly
- Debugging async code issues
- Optimizing async performance

## Do not use this skill when

- The task is unrelated to rust async patterns
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER perform blocking synchronous operations inside asynchronous event loops.
- NEVER perform blocking synchronous operations inside asynchronous event loops.
- NEVER run python applications without pinning exact dependencies in requirements or pyproject files.

## 6) Capture Knowledge

After a Rust async pattern implementation or concurrent system design is completed, automatically trigger the `capture_knowledge.py` script.
The script will analyze the async patterns to identify:
- Key async task structures and channel types.
- Error handling strategies and result types.
- Concurrency patterns and shared state management.
The script will then route this information to the appropriate storage:
- **OKF**: High-level async patterns, concurrency standards, and system designs.
- **ChromaDB**: Specific task definitions, error handling logic, and performance notes.
