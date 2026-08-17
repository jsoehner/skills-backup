---
name: microservices-patterns
description: Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems, decomposing monoliths, or implementing microservices.
---

# Microservices Patterns

Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems.

## Use this skill when

- Decomposing monoliths into microservices
- Designing service boundaries and contracts
- Implementing inter-service communication
- Managing distributed data and transactions
- Building resilient distributed systems
- Implementing service discovery and load balancing
- Designing event-driven architectures

## Do not use this skill when

- The system is small enough for a modular monolith
- You need a quick prototype without distributed complexity
- There is no operational support for distributed systems

## Instructions

1. Identify domain boundaries and ownership for each service.
2. Define contracts, data ownership, and communication patterns.
3. Plan resilience, observability, and deployment strategy.
4. Provide migration steps and operational guardrails.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.

## Knowledge Capture Requirement
When completing a task that involves a significant architectural decision, a complex bug fix, or a new infrastructure pattern, you MUST:
1. Synthesize the decision/fix into a concise summary (3-5 sentences).
2. Classify it as either **OKF** (High-level policy, architectural rule, or cross-cutting standard) or **CHROMA** (Technical context, implementation detail, or specific bug fix).
3. Execute `capture_knowledge.py` with the appropriate `--type` flag.
4. Ensure the captured knowledge is deduplicated and properly chunked using the `smart_chunk` logic.
