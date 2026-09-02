---
name: similarity-search-patterns
description: Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance.
---

# Similarity Search Patterns

Patterns for implementing efficient similarity search in production systems.

## Use this skill when

- Building semantic search systems
- Implementing RAG retrieval
- Creating recommendation engines
- Optimizing search latency
- Scaling to millions of vectors
- Combining semantic and keyword search

## Do not use this skill when

- The task is unrelated to similarity search patterns
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

After a security audit, risk assessment, or threat model is completed, automatically trigger the `capture_knowledge.py` script.
The script will analyze the security findings to identify:
- Key security rules, compliance standards, and risk profiles.
- Critical vulnerabilities, threat vectors, and mitigation strategies.
- Regulatory requirements (GDPR, HIPAA, etc.) and policy-level decisions.
The script will then route this information to the appropriate storage:
- **OKF**: High-level security policies, compliance standards, and corporate security rules.
- **ChromaDB**: Specific audit reports, vulnerability logs, and threat model details.