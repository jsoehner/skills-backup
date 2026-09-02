---
name: tailwind-design-system
description: Build scalable design systems with Tailwind CSS, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns.
---

# Tailwind Design System

Build production-ready design systems with Tailwind CSS, including design tokens, component variants, responsive patterns, and accessibility.

## Use this skill when

- Creating a component library with Tailwind
- Implementing design tokens and theming
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating to or extending Tailwind CSS
- Setting up dark mode and color schemes

## Do not use this skill when

- The task is unrelated to tailwind design system
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER load massive datasets directly into client memory; use pagination or infinite scroll.
- NEVER use generic, unstyled components or default browser styling in production-ready UIs.

## 6) Capture Knowledge

After a security audit, risk assessment, or threat model is completed, automatically trigger the `capture_knowledge.py` script.
The script will analyze the security findings to identify:
- Key security rules, compliance standards, and risk profiles.
- Critical vulnerabilities, threat vectors, and mitigation strategies.
- Regulatory requirements (GDPR, HIPAA, etc.) and policy-level decisions.
The script will then route this information to the appropriate storage:
- **OKF**: High-level security policies, compliance standards, and corporate security rules.
- **ChromaDB**: Specific audit reports, vulnerability logs, and threat model details.