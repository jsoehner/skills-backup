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

## 6) Memory Sync

After a Bats test suite is designed, a script is unit-tested, or a CI/CD test pipeline is completed, you **MUST** trigger the local memory capture. 

1. Save the final test plan, test suite, or CI/CD test configuration as a Markdown file in the project directory.
2. Invoke the capture script: 
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that test patterns, test suites, and CI/CD testing configurations are automatically routed to the correct storage (OKF or ChromaDB).

