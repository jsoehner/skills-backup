# Contributing to YUV AI Skills

Thank you for contributing to the YUV AI Skills repository! This project aims to provide a modular, scalable, and deployable collection of AI skills for various harnesses.

## Architecture Overview

### Atomic Skills
Located in the `skills/` directory, these are self-contained building blocks. They should not have dependencies on other skills in this repository.

### Composite Skills
Located in the root directory, these are orchestrators that depend on Atomic or other Composite skills.
- Each Composite skill **must** have a `manifest.json` file.
- Each Composite skill **must** list its dependencies in the `dependencies` section of its `SKILL.md` file.

## Contribution Workflow

### 1. Adding a New Skill
1. **Identify Type**: Determine if the skill is Atomic or Composite.
2. **Create Directory**: Create a new folder for the skill.
3. **Write SKILL.md**: Follow the provided templates to document the skill's goal, inputs, workflow, and references.
4. **Atomic Skills**: Place in the appropriate sub-folder within `skills/`.
5. **Composite Skills**:
    - Place in the root directory.
    - Create a `manifest.json` file with the required metadata.
    - Explicitly list dependencies in `SKILL.md`.
6. **Update Audit**: Record the new skill in `audit_status.json`.

### 2. Updating Existing Skills
1. **Review Requirements**: Ensure the skill still meets its stated goal.
2. **Update SKILL.md**: Reflect any changes in logic, inputs, or dependencies.
3. **Update manifest.json**: If dependencies or metadata have changed.
4. **Verification**: Run the skill (if possible) or verify the logic with the `skill-judge` skill.

### 3. Deployment
Use `deploy_skills.py` to verify that your changes don't break the dependency graph for the target harnesses.

## Code of Conduct
We expect all contributors to be respectful and professional. Please keep discussions constructive and focused on the technical goals of the project.
