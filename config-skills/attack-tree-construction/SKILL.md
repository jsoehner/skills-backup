---
name: attack-tree-construction
description: Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders.
---

# Attack Tree Construction

Systematic attack path visualization and analysis.

## Use this skill when

- Visualizing complex attack scenarios
- Identifying defense gaps and priorities
- Communicating risks to stakeholders
- Planning defensive investments or test scopes

## Do not use this skill when

- You lack authorization or a defined scope to model the system
- The task is a general risk review without attack-path modeling
- The request is unrelated to security assessment or design

## Instructions

- Confirm scope, assets, and the attacker goal for the root node.
- Decompose into sub-goals with AND/OR structure.
- Annotate leaves with cost, skill, time, and detectability.
- Map mitigations per branch and prioritize high-impact paths.
- If detailed templates are required, open `resources/implementation-playbook.md`.

## Safety

- Share attack trees only with authorized stakeholders.
- Avoid including sensitive exploit details unless required.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, templates, and examples.

## Anti-Patterns

- NEVER publish attack trees to public repositories or unauthorized personnel.
- NEVER include specific zero-day details or functional exploit scripts in the tree annotations.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
