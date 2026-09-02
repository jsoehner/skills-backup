---
name: "install-adr-gatekeeper"
description: "Installs the ADR Gatekeeper system into the current project, including indexing, significance rules, and CI/CD integration."
version: 1
created: "2026-08-12"
updated: "2026-08-12"
---

## When to Use

Use this skill when deploying the **ADR Gatekeeper** system into any repository to enforce automated architectural governance. The gatekeeper automatically inspects code diffs in pre-commit hooks and CI/CD pull request pipelines to detect Architecturally Significant Requirements (ASRs) and verify that an ADR exists in `docs/adr/`.

---

## Deployment Blueprint & File Hierarchy

Deploying the ADR Gatekeeper provisions the following assets:

```text
<project-root>/
├── docs/adr/
│   ├── adr_index.json              # Dynamic machine-readable ADR decision register
│   ├── adr_analyst_config.json     # Significance detection rules & sensitivity thresholds
│   └── adr_analyst_prompt.txt      # LLM Gatekeeper persona & ASR analysis prompt
├── scripts/
│   └── adr_gatekeeper.py           # Automated evaluation & verification CLI engine
├── .github/workflows/
│   └── adr-gatekeeper.yml          # GitHub Actions pull request gatekeeping workflow
└── .git/hooks/
    └── pre-commit                  # Local git pre-commit hook enforcement
```

---

## Step-by-Step Deployment Procedure

### Step 1: Initialize Required Directories
Ensure the base directories exist:
```bash
mkdir -p docs/adr/templates scripts .github/workflows
```

### Step 2: Provision `docs/adr/adr_index.json`
Create the initial decision registry tracking all approved ADRs:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "version": "1.0.0",
  "adrs": [
    {
      "id": "0000",
      "title": "Record Architecture Decisions",
      "status": "Accepted",
      "date": "2026-09-02",
      "file": "docs/adr/0000-record-architecture-decisions.md",
      "tags": ["governance", "standards"]
    }
  ]
}
```

### Step 3: Provision `docs/adr/adr_analyst_config.json`
Define the trigger heuristics and sensitivity patterns:
```json
{
  "version": "1.0.0",
  "asr_triggers": {
    "sensitive_paths": [
      "src/core/**",
      "src/auth/**",
      "infra/**",
      "terraform/**",
      "k8s/**",
      "migrations/**",
      "schema/**",
      "proto/**"
    ],
    "architectural_keywords": [
      "BREAKING CHANGE",
      "deprecate",
      "protocol change",
      "database migration",
      "auth provider",
      "encryption",
      "microservice",
      "zero trust"
    ],
    "thresholds": {
      "max_unreviewed_core_loc": 250,
      "require_adr_for_new_services": true,
      "require_adr_for_schema_changes": true
    }
  },
  "adr_directory": "docs/adr",
  "index_file": "docs/adr/adr_index.json"
}
```

### Step 4: Provision `docs/adr/adr_analyst_prompt.txt`
Configure the LLM gatekeeper persona:
```text
You are the ADR Gatekeeper Analyst. Your mission is to eliminate "Architecture by Accident" by analyzing git changesets against Architecturally Significant Requirements (ASRs).

Evaluate changes across four primary axes:
1. Quality Attributes: Non-functional changes (latency, scale, cost, security).
2. System Constraints: Organizational, regulatory, or platform dependencies.
3. Scope & Communication Boundaries: New API contracts, DB schemas, or network topologies.
4. Reversibility Cost: Difficulty/cost to revert or alter in 6+ months.

If the change crosses an ASR threshold, you must ensure a corresponding record is authored in docs/adr/ using the appropriate template from docs/adr/templates/.
```

### Step 5: Provision `scripts/adr_gatekeeper.py`
Create the standalone Python gatekeeper CLI:
```python
#!/usr/bin/env python3
"""ADR Gatekeeper CLI - Analyzes git diffs for architectural significance and enforces ADR compliance."""

import json
import os
import subprocess
import sys
import fnmatch

CONFIG_PATH = os.environ.get("ADR_CONFIG_PATH", "docs/adr/adr_analyst_config.json")
ADR_DIR = os.environ.get("ADR_DIR", "docs/adr")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_staged_or_pr_diff(base_branch=None):
    if base_branch:
        cmd = ["git", "diff", f"origin/{base_branch}...HEAD", "--name-only"]
    else:
        cmd = ["git", "diff", "--cached", "--name-only"]
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    except subprocess.CalledProcessError:
        return []

def evaluate_files(files, config):
    triggers = config.get("asr_triggers", {})
    sensitive_patterns = triggers.get("sensitive_paths", [])
    
    flagged_files = []
    adr_modified = False

    for file_path in files:
        if file_path.startswith("docs/adr/") and file_path.endswith(".md") and not file_path.endswith("README.md"):
            adr_modified = True
            continue
        
        for pattern in sensitive_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                flagged_files.append((file_path, pattern))
                break

    return flagged_files, adr_modified

def main():
    base_branch = sys.argv[1] if len(sys.argv) > 1 else None
    config = load_config()
    changed_files = get_staged_or_pr_diff(base_branch)

    if not changed_files:
        print("✅ [ADR Gatekeeper] No changed files detected.")
        sys.exit(0)

    flagged, adr_modified = evaluate_files(changed_files, config)

    if flagged and not adr_modified:
        print("⚠️  [ADR Gatekeeper] Architecturally significant changes detected without a corresponding ADR:")
        for f, pat in flagged:
            print(f"   - {f} (matched pattern: '{pat}')")
        print("\n👉 Please document this architectural decision in docs/adr/ using an appropriate template from docs/adr/templates/.")
        print("   Run `adr-discovery` or `adr-authoring` to generate the record.")
        sys.exit(1)
    
    print("✅ [ADR Gatekeeper] Architectural governance verification passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Step 6: Provision `.github/workflows/adr-gatekeeper.yml`
Configure GitHub Actions pull request automation:
```yaml
name: ADR Gatekeeper

on:
  pull_request:
    branches: [ main, master, develop ]

jobs:
  verify-adr-compliance:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run ADR Gatekeeper
        run: |
          chmod +x scripts/adr_gatekeeper.py
          python3 scripts/adr_gatekeeper.py ${{ github.base_ref }}
```

### Step 7: Configure Pre-Commit Hook
Enable local pre-commit checks:
```bash
cat << 'EOF' > .git/hooks/pre-commit
#!/usr/bin/env bash
if [ -f scripts/adr_gatekeeper.py ]; then
    python3 scripts/adr_gatekeeper.py
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo "❌ Pre-commit hook aborted due to unrecorded architectural changes."
        exit $EXIT_CODE
    fi
fi
EOF
chmod +x .git/hooks/pre-commit
```

---

## Verification & Testing
1. **Script Validation**: Run `python3 scripts/adr_gatekeeper.py` with clean and staged changes.
2. **CI Simulation**: Test against base branch: `python3 scripts/adr_gatekeeper.py main`.
3. **Pre-commit Trigger**: Test local commit rejection when modifying a sensitive path without staging a file in `docs/adr/`.

---

## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
