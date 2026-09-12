#!/usr/bin/env python3
"""
Pre-Commit Security & ADR Gatekeeper (Cross-Platform Python)
Runs on Windows, macOS, and Linux.

Checks staged git files for:
1. Plaintext credentials, private keys, and API tokens.
2. Security-sensitive architectural changes that require an accompanying ADR.
"""

import sys
import re
import subprocess
from pathlib import Path

# Common high-entropy or recognizable secret patterns
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"gho_[0-9a-zA-Z]{36}", "GitHub OAuth Token"),
    (r"-----BEGIN (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "Private Encryption Key"),
    (r"eyJhbGciOi[0-9a-zA-Z_-]{10,}\.[0-9a-zA-Z_-]{10,}\.[0-9a-zA-Z_-]{10,}", "JSON Web Token (JWT)"),
    (r"sk_live_[0-9a-zA-Z]{24}", "Stripe Live API Key"),
    (r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,32}", "Slack Token"),
]

SENSITIVE_PATHS = [
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
        return ""

def main():
    print("🔒 [Security Governance] Running cross-platform pre-commit checks...")

    # Get staged files
    staged_output = run_git(["diff", "--cached", "--name-only", "--diff-filter=ACM"])
    if not staged_output:
        sys.exit(0)

    staged_files = [line.strip().replace("\\", "/") for line in staged_output.splitlines() if line.strip()]
    if not staged_files:
        sys.exit(0)

    # 1. Scan staged diffs for plaintext secrets
    found_secrets = []
    for filepath in staged_files:
        diff_text = run_git(["diff", "--cached", filepath])
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, diff_text):
                found_secrets.append((filepath, desc))

    if found_secrets:
        print("\n❌ SECURITY GATE FAILURE: Plaintext credentials detected in staged commit!")
        for f, desc in found_secrets:
            print(f"   - {f}: Detected {desc}")
        print("\nPlease remove the credentials, revoke if exposed, and use environment variables or secret vaults.")
        sys.exit(1)

    # 2. Check for security-sensitive architectural changes
    touches_sensitive = []
    for f in staged_files:
        for prefix in SENSITIVE_PATHS:
            if f.startswith(prefix):
                touches_sensitive.append(f)
                break

    if touches_sensitive:
        has_adr = any(f.startswith("docs/adr/") and f.endswith(".md") for f in staged_files)
        if not has_adr:
            print("\n⚠️  ARCHITECTURAL NOTICE: Staged changes touch security-critical boundaries:")
            for f in touches_sensitive[:5]:
                print(f"   - {f}")
            if len(touches_sensitive) > 5:
                print(f"   - ... and {len(touches_sensitive) - 5} other files")
            print("   No accompanying ADR found in 'docs/adr/'.")
            print("   Ensure this architectural change is documented in docs/adr/ before opening a PR.")
            print("   (CI will enforce ADR presence on protected branches).\n")

    print("✅ [Security Governance] Pre-commit checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
