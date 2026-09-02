---
name: sql-optimization-patterns
description: Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries. Use when debugging slow queries, designing database schemas, or optimizing application performance.
---

# SQL Optimization Patterns

Transform slow database queries into lightning-fast operations through systematic optimization, proper indexing, and query plan analysis.

## Use this skill when

- Debugging slow-running queries
- Designing performant database schemas
- Optimizing application response times
- Reducing database load and costs
- Improving scalability for growing datasets
- Analyzing EXPLAIN query plans
- Implementing efficient indexes
- Resolving N+1 query problems

## Do not use this skill when

- The task is unrelated to sql optimization patterns
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER execute raw DML/DDL operations on production database instances without verification.
- NEVER ignore connection limits and connection pool starvation indicators.

## 6) Capture Knowledge

After a security audit, risk assessment, or threat model is completed, automatically trigger the `capture_knowledge.py` script.
The script will analyze the security findings to identify:
- Key security rules, compliance standards, and risk profiles.
- Critical vulnerabilities, threat vectors, and mitigation strategies.
- Regulatory requirements (GDPR, HIPAA, etc.) and policy-level decisions.
The script will then route this information to the appropriate storage:
- **OKF**: High-level security policies, compliance standards, and corporate security rules.
- **ChromaDB**: Specific audit reports, vulnerability logs, and threat model details.