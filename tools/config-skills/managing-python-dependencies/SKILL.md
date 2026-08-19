---
name: managing-python-dependencies
description: |
  Ensures proper Python dependency management, avoiding global `pip install` and
  adhering to project-specific tooling.

  Use this skill if any of the following are true:
    1. Attempting to run `pip install {package_name}`.
    2. Python packages or dependencies need to be added or modified.
    3. Initiating a new Python project.
    4. Creating a new notebook, even if just using BigQuery cells.
    5. Generating Python code that includes `import` statements for third-party libraries.
    6. Before executing Python scripts via the terminal to ensure the correct virtual environment is active.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# Python Dependency Management Rule

> [!CAUTION]
>
> **BEFORE any `pip install`**: You MUST first detect the project's existing
> dependency manager and use it correctly. Do NOT override the project's
> established tooling.

## Dependency Manager Detection

Before installing ANY Python package, check the workspace for these files **in
priority order**:

1.  **Signal:** `uv.lock` or `pyproject.toml` with `[tool.uv]`
    *   **Tool:** **uv**
    *   **Install:** `uv add <package>`
    *   **Setup:** `uv sync`
2.  **Signal:** `pyproject.toml` with `[tool.poetry]`
    *   **Tool:** **Poetry**
    *   **Install:** `poetry add <package>`
    *   **Setup:** `poetry install`
3.  **Signal:** `Pipfile`
    *   **Tool:** **Pipenv**
    *   **Install:** `pipenv install <package>`
    *   **Setup:** `pipenv install`
4.  **Signal:** `environment.yml`
    *   **Tool:** **Conda**
    *   **Install:** `conda install <package>`
    *   **Setup:** `conda env create -f environment.yml`
5.  **Signal:** `requirements.txt` only
    *   **Tool:** **venv + pip**
    *   **Install:** `.venv/bin/pip install <package>`
    *   **Setup:** `.venv/bin/pip install -r requirements.txt`
6.  **Signal:** None of the above
    *   **Tool:** **venv + pip** (default)
    *   **Install:** `.venv/bin/pip install <package>`
    *   **Setup:** `.venv/bin/pip install -r requirements.txt`

## Default: venv + pip

If no dependency manager is detected, use **venv + pip** as
the default:

```bash
# Initialize environment
python3 -m venv .venv

# Add dependencies
.venv/bin/pip install <package>

# Preserve state
.venv/bin/pip freeze > requirements.txt
```

**Rules for venv + pip workflow:**

-   Always use `.venv/bin/pip` or `.venv/bin/python` (explicit path).
-   After installing, run: `.venv/bin/pip freeze > requirements.txt`.
-   When setting up: `.venv/bin/pip install -r requirements.txt`.

## Prohibited

-   **NEVER** run `pip install` globally
-   **NEVER** override an existing dependency manager with a different one\\

## Anti-Patterns

- NEVER perform blocking synchronous operations inside asynchronous event loops.
- NEVER run python applications without pinning exact dependencies in requirements or pyproject files.

## 6) Capture Knowledge

After a new Python dependency is added or the project's dependency manager is configured, automatically trigger the `capture_knowledge.py` script.
The script will analyze the dependency changes to identify:
- New package additions and their purpose.
- Dependency version updates or major version bumps.
- New project-wide configuration in `pyproject.toml`, `Pipfile`, or `requirements.txt`.
The script will then route this information to the appropriate storage:
- **OKF**: High-level Python environment standards and dependency management rules.
- **ChromaDB**: Specific package lists, version constraints, and dependency-related configurations.
",path: