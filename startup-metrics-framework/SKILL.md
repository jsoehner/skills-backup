---
name: startup-metrics-framework
description: This skill should be used when the user asks about "key startup
  metrics", "SaaS metrics", "CAC and LTV", "unit economics", "burn multiple",
  "rule of 40", "marketplace metrics", or requests guidance on tracking and
  optimizing business performance metrics.
metadata:
  version: 1.0.0
---

# Startup Metrics Framework

Comprehensive guide to tracking, calculating, and optimizing key performance metrics for different startup business models from seed through Series A.

## Use this skill when

- Working on startup metrics framework tasks or workflows
- Needing guidance, best practices, or checklists for startup metrics framework

## Do not use this skill when

- The task is unrelated to startup metrics framework
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

After the analysis or business case is finalized, automatically trigger the `capture_knowledge.py` script.
The script will analyze the findings and identify:
- Key market opportunities and "10x" opportunities.
- High-level strategic decisions and "Hard Rules" for the business model.
- Key financial targets and unit economics milestones.
The script will then route this information to the appropriate storage:
- **OKF**: High-level strategy, market sizing conclusions, and business model rules.
- **ChromaDB**: Specific financial model scenarios, competitive analysis details, and detailed startup metrics.