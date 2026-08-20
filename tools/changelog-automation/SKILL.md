---

name: changelog-automation

description: Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions.

---



# Changelog Automation



Patterns and tools for automating changelog generation, release notes, and version management following industry standards.



## Use this skill when



- Setting up automated changelog generation

- Implementing conventional commits

- Creating release note workflows

- Standardizing commit message formats

- Managing semantic versioning



## Do not use this skill when



- The project has no release process or versioning

- You only need a one-time manual release note

- Commit history is unavailable or unreliable



## Instructions



- Select a changelog format and versioning strategy.

- Enforce commit conventions or labeling rules.

- Configure tooling to generate and publish notes.

- Review output for accuracy, completeness, and wording.

- If detailed examples are required, open `resources/implementation-playbook.md`.



## Safety



- Avoid exposing secrets or internal-only details in release notes.



## Resources



- `resources/implementation-playbook.md` for detailed patterns, templates, and examples.



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
