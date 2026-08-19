---
name: employment-contract-templates
description: Create employment contracts, offer letters, and HR policy documents following legal best practices. Use when drafting employment agreements, creating HR policies, or standardizing employment documentation.
---

# Employment Contract Templates

Templates and patterns for creating legally sound employment documentation including contracts, offer letters, and HR policies.

## Use this skill when

- Drafting employment contracts
- Creating offer letters
- Writing employee handbooks
- Developing HR policies
- Standardizing employment documentation
- Preparing onboarding documentation

## Do not use this skill when

- You need jurisdiction-specific legal advice
- The task requires licensed counsel review
- The request is unrelated to employment documentation

## Instructions

- Confirm jurisdiction, employment type, and required clauses.
- Choose a document template and tailor role-specific terms.
- Validate compensation, benefits, and compliance requirements.
- Add signature, confidentiality, and IP assignment terms as needed.
- If detailed templates are required, open `resources/implementation-playbook.md`.

## Safety

- These templates are not legal advice; consult qualified counsel before use.

## Resources

- `resources/implementation-playbook.md` for detailed templates and checklists.

## Anti-Patterns

- NEVER deploy code changes without validating them against target test suites.
- NEVER skip documenting non-obvious code assumptions, constraints, and side effects.

## 6) Memory Sync

Execute the following steps to sync knowledge to the memory system:
1. Use `capture_knowledge.py` to route information to the correct storage (OKF or ChromaDB).
2. Ensure that high-level architectural rules, policies, and decisions are stored in the OKF (Open Knowledge Format) directory.
3. Ensure that ephemeral data, logs, and specific technical notes are stored in the ChromaDB instance.
4. Verify that the `MEMORY_SYSTEM_ROOT` and `MEMORY_INBOX_DIR` environment variables are correctly configured.
