#!/usr/bin/env python3
"""
ADR Security Gatekeeper (Cross-Platform Python)
Analyzes Git changes (pull request diff, branch diff, or staged files)
and enforces that changes to security-critical architecture paths must include
an Architectural Decision Record (ADR) in docs/adr/.

Usage:
    python adr_security_gatekeeper.py [--base origin/main] [--staged] [--event pull_request]
"""

import sys
import argparse
import subprocess
from pathlib import Path

DEFAULT_SENSITIVE_PATHS = [
    "auth/",
    "crypto/",
    "security/",
    "certs/",
    ".github/workflows/",
    "api/",
    "policy/",
]

def run_git(args):
    try:
        res = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git command error ('git {' '.join(args)}'): {e.stderr.strip()}", file=sys.stderr)
        return ""

def get_changed_files(base_branch=None, staged=False):
    if staged:
        output = run_git(["diff", "--cached", "--name-only", "--diff-filter=ACM"])
    elif base_branch:
        output = run_git(["diff", "--name-only", f"{base_branch}...HEAD"])
        if not output:
            # Fallback if three-dot diff fails or returns empty
            output = run_git(["diff", "--name-only", base_branch, "HEAD"])
    else:
        # Default to checking against HEAD~1 or uncommitted changes
        output = run_git(["diff", "--name-only", "HEAD~1", "HEAD"])

    files = [f.strip().replace("\\", "/") for f in output.splitlines() if f.strip()]
    return files

def main():
    parser = argparse.ArgumentParser(description="Enforce ADR requirements on security-sensitive changes.")
    parser.add_argument("--base", default=None, help="Base branch to compare against (e.g. origin/main)")
    parser.add_argument("--staged", action="store_true", help="Check staged files instead of commit range")
    parser.add_argument("--event", default="pull_request", help="Triggering event (pull_request, push, etc.)")
    parser.add_argument("--paths", nargs="*", default=DEFAULT_SENSITIVE_PATHS, help="List of sensitive path prefixes")
    args = parser.parse_args()

    print("🛡️ [ADR Security Gatekeeper] Analyzing changes...")

    changed_files = get_changed_files(base_branch=args.base, staged=args.staged)

    if not changed_files:
        print("ℹ️ No files changed in analyzed scope.")
        sys.exit(0)

    print(f"Total changed files: {len(changed_files)}")

    # Check for sensitive paths
    sensitive_modified = []
    for f in changed_files:
        for prefix in args.paths:
            if f.startswith(prefix):
                sensitive_modified.append(f)
                break

    if not sensitive_modified:
        print("✅ No security-critical architecture paths modified. ADR not required.")
        sys.exit(0)

    print("\n⚠️ Security-critical files modified in this change set:")
    for f in sensitive_modified:
        print(f"   - {f}")

    # Check for ADR update
    adr_files = [f for f in changed_files if f.startswith("docs/adr/") and f.endswith(".md") and not f.endswith("README.md")]

    if adr_files:
        print(f"\n✅ Architectural Decision Record(s) found in docs/adr/:")
        for adr in adr_files:
            print(f"   + {adr}")
        print("\n🎉 ADR Gatekeeper check passed!")
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("❌ ERROR: ADR SECURITY GATEKEEPER CHECK FAILED")
        print("=" * 70)
        print("Changes touch security-sensitive paths, but no Architectural Decision Record")
        print("was added or updated in 'docs/adr/'.")
        print("\nRemediation:")
        print("  1. Review 'docs/adr/Security_ADR_Template.md'")
        print("  2. Create a new ADR (e.g. 'docs/adr/000X-security-decision-name.md')")
        print("  3. Update 'docs/adr/README.md' index table")
        print("  4. Commit the ADR alongside your changes.")
        print("=" * 70 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
