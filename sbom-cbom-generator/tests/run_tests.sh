#!/usr/bin/env bash
# ==============================================================================
# run_tests.sh - Comprehensive Test Suite for sbom-cbom-generator
# ==============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="/home/jsoehner/.gemini/config/skills/skill-creator/scripts/quick_validate.py"

echo "=================================================================="
echo " Running Test Suite for Skill: sbom-cbom-generator"
echo "=================================================================="

# 1. Structural Validation (validate_skill.py)
echo -n "[1/3] Validating Skill structure and frontmatter ... "
VALIDATOR="${SKILL_DIR}/tests/validate_skill.py"
if python3 "$VALIDATOR" "$SKILL_DIR" >/dev/null 2>&1; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
    python3 "$VALIDATOR" "$SKILL_DIR"
    exit 1
fi

# 2. CLI Interface Tests (test_generate_script.sh)
echo "[2/3] Running CLI interface tests ..."
bash "${SKILL_DIR}/tests/test_generate_script.sh"
echo "✅ PASSED"

# 3. CBOM Analyzer Unit Tests (test_cbom_analysis.py)
echo "[3/3] Running CBOM analyzer Python unit tests ..."
python3 "${SKILL_DIR}/tests/test_cbom_analysis.py"
echo "✅ PASSED"

echo "=================================================================="
echo "🎉 ALL TESTS PASSED SUCCESSFULLY!"
echo "=================================================================="
