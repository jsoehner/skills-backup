#!/usr/bin/env bash
# ==============================================================================
# test_generate_script.sh - Validation of generate_boms.sh CLI interface
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${SKILL_DIR}/scripts/generate_boms.sh"

echo "=== Testing generate_boms.sh CLI ==="

# 1. Test help flag (should exit 0 with usage)
echo -n "Test 1: Help flag ... "
HELP_OUT="$("$SCRIPT" --help 2>&1)" || true
if echo "$HELP_OUT" | grep -q "Usage:"; then
    echo "PASSED"
else
    echo "FAILED"
    exit 1
fi

# 2. Test missing target (should exit 1 with error)
echo -n "Test 2: Missing target error ... "
set +e
ERR_OUT="$("$SCRIPT" 2>&1)"
RET=$?
set -e
if [[ $RET -ne 0 ]] && echo "$ERR_OUT" | grep -q "Error: Target is required"; then
    echo "PASSED"
else
    echo "FAILED (exit code: $RET)"
    exit 1
fi

# 3. Test unknown option (should exit 1)
echo -n "Test 3: Unknown option error ... "
set +e
ERR_OUT="$("$SCRIPT" --invalid-option 2>&1)"
RET=$?
set -e
if [[ $RET -ne 0 ]] && echo "$ERR_OUT" | grep -q "Error: Unknown option"; then
    echo "PASSED"
else
    echo "FAILED (exit code: $RET)"
    exit 1
fi

echo "All CLI interface tests PASSED successfully!"
