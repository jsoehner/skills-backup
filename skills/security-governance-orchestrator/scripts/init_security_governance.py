#!/usr/bin/env python3
"""
Initialize complete Security Governance, ADR framework, and GitHub Security Workflows for any repository.
Usage:
    python3 init_security_governance.py [target_repo_path]
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import date

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_ROOT / "templates"

def init_repo(target_dir_str: str):
    target_dir = Path(target_dir_str).resolve()
    if not target_dir.exists():
        print(f"❌ Error: Target directory does not exist: {target_dir}")
        sys.exit(1)

    print(f"🛡️ Initializing Security Governance in: {target_dir}")
    today_str = date.today().isoformat()

    # 1. Create docs/adr/ directory and baseline files
    adr_dir = target_dir / "docs" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)

    adr_0000 = adr_dir / "0000-record-architecture-decisions.md"
    if not adr_0000.exists():
        adr_0000.write_text(f"""# 0. Record Architecture Decisions

- **Status**: Accepted
- **Date**: {today_str}
- **Security Classification**: Internal
- **Decision Makers**: Architecture Review Board & Security Team

## Context
We need to record architecturally significant decisions, security controls, cryptographic choices, and compliance exception rationale.

## Decision
We will use Architectural Decision Records (ADRs) and Security ADRs stored directly in `docs/adr/`. All significant design choices affecting security, data boundaries, or system architecture must be documented here.

## Consequences
- Architectural rationale and security decisions are preserved in git.
- Pull requests modifying security-sensitive architecture are checked for corresponding ADRs.
- Superseded decisions will be linked bidirectionally.
""")
        print("  ✅ Created docs/adr/0000-record-architecture-decisions.md")

    adr_readme = adr_dir / "README.md"
    if not adr_readme.exists():
        adr_readme.write_text(f"""# Architecture & Security Decision Log

This directory contains Architectural Decision Records (ADRs) and Security Architecture Decision Records (SecADRs) for this repository.

## Index of Decisions

| ID | Title | Date | Status | Classification |
| :--- | :--- | :--- | :--- | :--- |
| 0000 | [Record Architecture Decisions](0000-record-architecture-decisions.md) | {today_str} | Accepted | Internal |
""")
        print("  ✅ Created docs/adr/README.md index")

    # Copy Security ADR template into docs/adr/templates/ if desired
    adr_template_target = adr_dir / "Security_ADR_Template.md"
    if (TEMPLATES_DIR / "Security_ADR_Template.md").exists() and not adr_template_target.exists():
        shutil.copy(TEMPLATES_DIR / "Security_ADR_Template.md", adr_template_target)
        print("  ✅ Added docs/adr/Security_ADR_Template.md")

    # 2. Setup GitHub Actions workflows (.github/workflows/)
    workflows_dir = target_dir / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    workflow_target = workflows_dir / "security-governance.yml"
    if not workflow_target.exists() and (TEMPLATES_DIR / "security-governance.yml").exists():
        shutil.copy(TEMPLATES_DIR / "security-governance.yml", workflow_target)
        print("  ✅ Deployed .github/workflows/security-governance.yml")

    # 3. Setup Dependabot (.github/dependabot.yml)
    dependabot_target = target_dir / ".github" / "dependabot.yml"
    if not dependabot_target.exists() and (TEMPLATES_DIR / "dependabot.yml").exists():
        shutil.copy(TEMPLATES_DIR / "dependabot.yml", dependabot_target)
        print("  ✅ Deployed .github/dependabot.yml")

    # 4. Setup CODEOWNERS (.github/CODEOWNERS)
    codeowners_target = target_dir / ".github" / "CODEOWNERS"
    if not codeowners_target.exists():
        codeowners_target.write_text("""# Security Governance CODEOWNERS
# Require review from security champions on high-risk paths

# Security and Cryptography
/auth/              @security-team
/crypto/            @security-team
/security/          @security-team
/certs/             @security-team

# CI/CD Workflows & Policies
/.github/workflows/ @platform-team @security-team
/.github/CODEOWNERS @security-team

# Architectural Decisions
/docs/adr/          @architecture-board @security-team
""")
        print("  ✅ Deployed .github/CODEOWNERS")

    # 5. Deploy ADR Security Gatekeeper scripts into repo scripts/
    repo_scripts_dir = target_dir / "scripts"
    repo_scripts_dir.mkdir(parents=True, exist_ok=True)
    
    scripts_dir = SKILL_ROOT / "scripts"
    for gk_name in ["adr_security_gatekeeper.py", "adr-security-gatekeeper.ps1"]:
        src_gk = scripts_dir / gk_name
        dest_gk = repo_scripts_dir / gk_name
        if src_gk.exists() and not dest_gk.exists():
            shutil.copy(src_gk, dest_gk)
            if gk_name.endswith(".py"):
                try:
                    os.chmod(dest_gk, 0o755)
                except Exception:
                    pass
            print(f"  ✅ Deployed scripts/{gk_name}")

    # 6. Setup client-side Git pre-commit hooks (if .git directory exists)
    git_hooks_dir = target_dir / ".git" / "hooks"
    if git_hooks_dir.exists():
        hook_files = [
            ("pre_commit.py", "pre_commit.py", True),
            ("pre-commit.ps1", "pre-commit.ps1", False),
            ("pre-commit.bat", "pre-commit.bat", False),
            ("pre-commit.sh", "pre-commit", True),
        ]
        for src_name, dest_name, make_exec in hook_files:
            src_file = TEMPLATES_DIR / src_name
            dest_file = git_hooks_dir / dest_name
            if src_file.exists():
                shutil.copy(src_file, dest_file)
                if make_exec:
                    try:
                        os.chmod(dest_file, 0o755)
                    except Exception:
                        pass
        print("  ✅ Configured cross-platform Git pre-commit hooks (Python, PowerShell, Bash, Batch)")

    print("\n🎉 Security Governance setup complete!")
    print("Next steps:")
    print(" 1. Run local ADR Gatekeeper: python3 scripts/adr_security_gatekeeper.py (or scripts\\adr-security-gatekeeper.ps1)")
    print(" 2. Conduct a STRIDE threat model on core data flows")
    print(" 3. Record decisions in docs/adr/ using the Security ADR template")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    init_repo(target)
