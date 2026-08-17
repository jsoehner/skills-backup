---
name: bats-testing-patterns
description: Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities.
---

# Bats Testing Patterns

Comprehensive guidance for writing comprehensive unit tests for shell scripts using Bats (Bash Automated Testing System), including test patterns, fixtures, and best practices for production-grade shell testing.

## Use this skill when

- Writing unit tests for shell scripts
- Implementing TDD for scripts
- Setting up automated testing in CI/CD pipelines
- Testing edge cases and error conditions
- Validating behavior across shell environments

## Do not use this skill when

- The project does not use shell scripts
- You need integration tests beyond shell behavior
- The goal is only linting or formatting

## Instructions

- Confirm shell dialects and supported environments.
- Set up a test structure with helpers and fixtures.
- Write tests for exit codes, output, and side effects.
- Add setup/teardown and run tests in CI.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER write Bats tests without proper cleanup traps; left-over test files can pollute subsequent runs.
- NEVER assert on stdout alone when verifying command failures; always verify exit codes explicitly.

## Knowledge Capture Requirement
When completing a task that involves a significant architectural decision, a complex bug fix, or a new infrastructure pattern, you MUST:
1. Synthesize the decision/fix into a concise summary (3-5 sentences).
2. Classify it as either **OKF** (High-level policy, architectural rule, or cross-cutting standard) or **CHROMA** (Technical context, implementation detail, or specific bug fix).
3. Execute `capture_knowledge.py` with the appropriate `--type` flag.
4. Ensure the captured knowledge is deduplicated and properly chunked using the `smart_chunk` logic.
