---
name: gdpr-data-handling
description: Implement GDPR-compliant data handling with consent management, data subject rights, and privacy by design. Use when building systems that process EU personal data, implementing privacy controls, or conducting GDPR compliance reviews.
---

# GDPR Data Handling

Practical implementation guide for GDPR-compliant data processing, consent management, and privacy controls.

## Use this skill when

- Building systems that process EU personal data
- Implementing consent management
- Handling data subject requests (DSRs)
- Conducting GDPR compliance reviews
- Designing privacy-first architectures
- Creating data processing agreements

## Do not use this skill when

- The task is unrelated to gdpr data handling
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
