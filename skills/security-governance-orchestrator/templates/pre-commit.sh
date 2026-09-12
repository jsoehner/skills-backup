#!/usr/bin/env bash
# ==============================================================================
# Git Pre-Commit Hook: Security Governance & ADR Gate
# ==============================================================================
set -e

# Prefer cross-platform Python implementation if available
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 &>/dev/null && [ -f "$HOOK_DIR/pre_commit.py" ]; then
  exec python3 "$HOOK_DIR/pre_commit.py"
elif command -v python &>/dev/null && [ -f "$HOOK_DIR/pre_commit.py" ]; then
  exec python "$HOOK_DIR/pre_commit.py"
fi

echo "🔒 Running Security Governance pre-commit checks (Bash fallback)..."

# 1. Check for common plaintext secret patterns in staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

# Regex patterns for secrets
SECRET_PATTERNS="(AKIA[0-9A-Z]{16}|ghp_[0-9a-zA-Z]{36}|BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY|eyJhbGciOi|sk_live_[0-9a-zA-Z]{24})"

FOUND_SECRET=false
for file in $STAGED_FILES; do
  # Avoid checking binary files or .git directory
  if git diff --cached "$file" | grep -E "$SECRET_PATTERNS" > /dev/null; then
    echo "❌ SECURITY ALERT: Potential hardcoded credential or private key detected in staged file: $file"
    FOUND_SECRET=true
  fi
done

if [ "$FOUND_SECRET" = true ]; then
  echo "Commit rejected by Security Governance hook. Remove sensitive credentials or configure environment variables."
  exit 1
fi

# 2. Check for security architecture modifications without ADR
SENSITIVE_DIRS="auth/ crypto/ security/ certs/ .github/workflows/ api/"
TOUCHES_SENSITIVE=false

for path in $SENSITIVE_DIRS; do
  if echo "$STAGED_FILES" | grep -E "^$path" > /dev/null; then
    TOUCHES_SENSITIVE=true
    break
  fi
done

if [ "$TOUCHES_SENSITIVE" = true ]; then
  # Check if docs/adr contains staged changes
  if ! echo "$STAGED_FILES" | grep -E "^docs/adr/.*\.md$" > /dev/null; then
    echo "⚠️ NOTICE: Staged changes touch security-critical components ($SENSITIVE_DIRS)."
    echo "   Ensure you have documented the decision in docs/adr/ or have an approved ADR."
    echo "   (To bypass this warning during local prototyping, use git commit --no-verify, but CI will enforce it)."
  fi
fi

echo "✅ Security Governance pre-commit checks passed."
exit 0
