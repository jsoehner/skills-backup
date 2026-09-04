---
name: data-quality-frameworks
description: Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts.
---

# Data Quality Frameworks

Production patterns for implementing data quality with Great Expectations, dbt tests, and data contracts to ensure reliable data pipelines.

## Use this skill when

- Implementing data quality checks in pipelines
- Setting up Great Expectations validation
- Building comprehensive dbt test suites
- Establishing data contracts between teams
- Monitoring data quality metrics
- Automating data validation in CI/CD

## Do not use this skill when

- The data sources are undefined or unavailable
- You cannot modify validation rules or schemas
- The task is unrelated to data quality or contracts

## Instructions

- Identify critical datasets and quality dimensions.
- Define expectations/tests and contract rules.
- Automate validation in CI/CD and schedule checks.
- Set alerting, ownership, and remediation steps.
- If detailed patterns are required, open `resources/implementation-playbook.md`.

## Safety

- Avoid blocking critical pipelines without a fallback plan.
- Handle sensitive data securely in validation outputs.

## Resources

- `resources/implementation-playbook.md` for detailed frameworks, templates, and examples.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
