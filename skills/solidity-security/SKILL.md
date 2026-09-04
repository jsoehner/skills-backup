---
name: solidity-security
description: Master smart contract security best practices to prevent common vulnerabilities and implement secure Solidity patterns. Use when writing smart contracts, auditing existing contracts, or implementing security measures for blockchain applications.
---

# Solidity Security

Master smart contract security best practices, vulnerability prevention, and secure Solidity development patterns.

## Use this skill when

- Writing secure smart contracts
- Auditing existing contracts for vulnerabilities
- Implementing secure DeFi protocols
- Preventing reentrancy, overflow, and access control issues
- Optimizing gas usage while maintaining security
- Preparing contracts for professional audits
- Understanding common attack vectors

## Do not use this skill when

- The task is unrelated to solidity security
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


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
