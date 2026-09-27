#!/usr/bin/env python3
"""
scaffold_governance.py - Master Scaffolding Engine for Repository Governance

Deploys the "Gold Standard" repository governance suite to any target repository:
- Developer Experience & Documentation (CONTRIBUTING.md, PR template)
- Workflow Automation (commit-lint, changelog)
- Security Pipeline (Semgrep SAST, Gitleaks secrets, Trivy containers, Node 24 SHA pinning)
- Dual-Engine Supply Chain & Cryptographic Governance (SBOM & CBOM, AST multi-language
  call-site discovery, automated verification test harness, and PQC migration assessment)

Usage:
  python3 scaffold_governance.py <target_repo_path> [options]

Modes:
  --mode full          (default) Deploy all DX, security, and dual-engine BOM components
  --mode bom-only      Deploy only the dual-engine SBOM/CBOM scanning pipeline & GitHub Action
  --mode security-only Deploy only the multi-layer security testing pipeline
  --mode dx-only       Deploy only documentation and commit linting
"""

import argparse
import os
import shutil
import stat
import sys
from pathlib import Path

def is_safe_subpath(target_path: Path, base_path: Path) -> bool:
    """Enforce path containment to prevent directory traversal."""
    try:
        target_path.resolve().relative_to(base_path.resolve())
        return True
    except ValueError:
        return False

def copy_file_safe(src: Path, dst: Path, force: bool = False, dry_run: bool = False, make_executable: bool = False) -> bool:
    """Safely copy a file ensuring destination path containment."""
    if not src.exists():
        print(f"⚠️ Source file missing: {src}", file=sys.stderr)
        return False

    if dst.exists() and not force:
        print(f"⏭️  Already exists (skipping, use --force to overwrite): {dst}")
        return False

    if dry_run:
        print(f"[DRY RUN] Would copy {src.name} -> {dst}")
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    if make_executable:
        current_perms = dst.stat().st_mode
        dst.chmod(current_perms | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"✅ Installed: {dst}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold repository governance and BOM scanning pipelines onto any codebase."
    )
    parser.add_argument("target", help="Path to target repository")
    parser.add_argument(
        "--mode",
        choices=["full", "bom-only", "security-only", "dx-only"],
        default="full",
        help="Scaffolding scope: full (default), bom-only, security-only, or dx-only"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in target repository"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without modifying filesystem"
    )
    parser.add_argument(
        "--app-name",
        default="",
        help="Application / image tag name (defaults to repository folder name)"
    )

    args = parser.parse_args()

    repo_dir = Path(args.target).resolve()
    if not repo_dir.exists() or not repo_dir.is_dir():
        print(f"❌ Error: Target repository directory does not exist: {repo_dir}", file=sys.stderr)
        sys.exit(1)

    skill_root = Path(__file__).resolve().parent.parent
    templates_dir = skill_root / "templates"
    scripts_template_dir = templates_dir / "scripts"

    if not templates_dir.exists():
        print(f"❌ Error: Templates directory not found at {templates_dir}", file=sys.stderr)
        sys.exit(1)

    app_name = args.app_name or repo_dir.name
    print("=" * 68)
    print(f"🏛️  Repository Governance Scaffolder")
    print(f"   Target: {repo_dir}")
    print(f"   Mode:   {args.mode.upper()}")
    print(f"   App:    {app_name}")
    print("=" * 68)

    installed_items = []

    # 1. DX & Documentation Scaffolding
    if args.mode in ("full", "dx-only"):
        print("\n[1/3] Scaffolding Documentation & Developer Experience...")
        # CONTRIBUTING.md
        contrib_dst = repo_dir / "CONTRIBUTING.md"
        if is_safe_subpath(contrib_dst, repo_dir):
            if copy_file_safe(templates_dir / "CONTRIBUTING.md", contrib_dst, args.force, args.dry_run):
                installed_items.append("CONTRIBUTING.md")

        # PR Template
        pr_dst = repo_dir / ".github" / "PULL_REQUEST_TEMPLATE.md"
        if is_safe_subpath(pr_dst, repo_dir):
            if copy_file_safe(templates_dir / "PULL_REQUEST_TEMPLATE.md", pr_dst, args.force, args.dry_run):
                installed_items.append(".github/PULL_REQUEST_TEMPLATE.md")

        # Commit lint & Changelog workflows
        cl_dst = repo_dir / ".github" / "workflows" / "commit-lint.yml"
        if is_safe_subpath(cl_dst, repo_dir):
            if copy_file_safe(templates_dir / "commit-lint.yml", cl_dst, args.force, args.dry_run):
                installed_items.append(".github/workflows/commit-lint.yml")

        ch_dst = repo_dir / ".github" / "workflows" / "changelog.yml"
        if is_safe_subpath(ch_dst, repo_dir):
            if copy_file_safe(templates_dir / "changelog.yml", ch_dst, args.force, args.dry_run):
                installed_items.append(".github/workflows/changelog.yml")

    # 2. Security Pipeline Scaffolding
    if args.mode in ("full", "security-only"):
        print("\n[2/3] Scaffolding Security Hardening & SAST Workflows...")
        sec_dst = repo_dir / ".github" / "workflows" / "security-testing.yml"
        if is_safe_subpath(sec_dst, repo_dir):
            if copy_file_safe(templates_dir / "security-testing.yml", sec_dst, args.force, args.dry_run):
                installed_items.append(".github/workflows/security-testing.yml")

    # 3. Dual-Engine BOM & Cryptographic Governance Scaffolding
    if args.mode in ("full", "bom-only"):
        print("\n[3/3] Scaffolding Dual-Engine SBOM/CBOM Suite & Verification CI...")
        scripts_to_install = [
            "generate_boms.sh",
            "scan_crypto_ast.py",
            "analyze_cbom.py",
            "test_boms.sh",
        ]

        target_scripts_dir = repo_dir / "scripts"
        for sname in scripts_to_install:
            src_script = scripts_template_dir / sname
            dst_script = target_scripts_dir / sname
            if is_safe_subpath(dst_script, repo_dir):
                if copy_file_safe(src_script, dst_script, args.force, args.dry_run, make_executable=True):
                    installed_items.append(f"scripts/{sname}")

        # SBOM & CBOM GitHub Action Workflow
        sbom_wf_dst = repo_dir / ".github" / "workflows" / "sbom.yml"
        if is_safe_subpath(sbom_wf_dst, repo_dir):
            if copy_file_safe(templates_dir / "sbom.yml", sbom_wf_dst, args.force, args.dry_run):
                installed_items.append(".github/workflows/sbom.yml")

    print("\n" + "=" * 68)
    if args.dry_run:
        print("🔍 Dry run completed. No files were written.")
    else:
        print(f"🎉 Governance suite scaffolding completed ({len(installed_items)} components applied).")
        print("\nLocal Verification Steps:")
        if args.mode in ("full", "bom-only"):
            print("  1. Run BOM generation and cryptographic scan:")
            print(f"     cd {repo_dir} && bash scripts/generate_boms.sh .")
            print("  2. Run automated validation test harness:")
            print(f"     cd {repo_dir} && bash scripts/test_boms.sh oss")
        print("=" * 68)

if __name__ == "__main__":
    main()
