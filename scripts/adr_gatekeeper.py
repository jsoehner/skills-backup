#!/usr/bin/env python3
"""ADR Gatekeeper CLI - Analyzes git diffs for architectural significance and enforces ADR compliance."""

import fnmatch
import json
import os
import subprocess
import sys

CONFIG_PATH = os.environ.get("ADR_CONFIG_PATH", "docs/adr/adr_analyst_config.json")
ADR_DIR = os.environ.get("ADR_DIR", "docs/adr")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  [ADR Gatekeeper] Warning: Could not parse config at {CONFIG_PATH}: {e}")
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
        # Fallback to local unstaged diff if not in pre-commit / staging
        cmd_fallback = ["git", "diff", "--name-only"]
        res = subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return [f.strip() for f in res.stdout.strip().split("\n") if f.strip()]

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

    print("🔍 [ADR Gatekeeper] Evaluating architectural compliance...")

    if not changed_files:
        print("✅ [ADR Gatekeeper] No changed files detected.")
        sys.exit(0)

    print(f"ℹ️  [ADR Gatekeeper] Inspecting {len(changed_files)} changed file(s)...")
    flagged, adr_modified = evaluate_files(changed_files, config)

    if flagged and not adr_modified:
        print("\n⚠️  [ADR Gatekeeper] Architecturally significant changes detected without a corresponding ADR in docs/adr/:")
        for f, pat in flagged:
            print(f"   • {f} (matched pattern: '{pat}')")
        print("\n👉 Please document this architectural decision in docs/adr/ using an appropriate template from docs/adr/templates/.")
        print("   Use `adr-discovery` or `adr-authoring` skills to generate the record, or stage an ADR alongside your changes.\n")
        sys.exit(1)
    
    if adr_modified:
        print("✨ [ADR Gatekeeper] Architectural Decision Record included with change.")

    print("✅ [ADR Gatekeeper] Architectural governance verification passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
