#!/usr/bin/env bash
# ==============================================================================
# install_to_repo.sh - Install SBOM/CBOM Generation & Test Harness into any Repo
# ==============================================================================
# Adds generation scripts, analysis tools, verification test harness,
# and GitHub Actions CI workflow to any target repository.
#
# Usage:
#   install_to_repo.sh [OPTIONS] <TARGET_REPO_PATH>
#
# Options:
#   -a, --app-name NAME     Application / Docker image name (default: detected or my-app)
#   -t, --type TYPE         Scan type: 'docker' or 'dir' (default: auto-detected)
#   -h, --help              Show this help message and exit
# ==============================================================================

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_REPO=""
APP_NAME=""
SCAN_TYPE=""

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] <TARGET_REPO_PATH>

Arguments:
  <TARGET_REPO_PATH>    Path to the target repository

Options:
  -a, --app-name NAME   Application or Docker image tag name (default: auto-detect)
  -t, --type TYPE       Scan type: 'docker' or 'dir' (default: auto-detect from Dockerfile)
  -h, --help            Show this help message and exit

Examples:
  $(basename "$0") .
  $(basename "$0") -a vault-demo -t docker /home/user/vaultpki-demo
EOF
    exit "${1:-1}"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -a|--app-name)
            APP_NAME="$2"
            shift 2
            ;;
        -t|--type)
            SCAN_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            usage 0
            ;;
        *)
            if [[ -z "$TARGET_REPO" ]]; then
                TARGET_REPO="$1"
                shift
            else
                echo "Error: Multiple target directories specified: '$TARGET_REPO' and '$1'" >&2
                usage 1
            fi
            ;;
    esac
done

if [[ -z "$TARGET_REPO" ]]; then
    echo "Error: Target repository path is required." >&2
    usage 1
fi

REPO_DIR="$(cd "$TARGET_REPO" && pwd)"

if [[ ! -d "$REPO_DIR" ]]; then
    echo "Error: Target directory does not exist: $TARGET_REPO" >&2
    exit 1
fi

echo "=================================================================="
echo " Installing SBOM & CBOM Generator + Test Harness into:"
echo " ${REPO_DIR}"
echo "=================================================================="

# Detect scan type if not specified
if [[ -z "$SCAN_TYPE" ]]; then
    if [[ -f "${REPO_DIR}/Dockerfile" ]]; then
        SCAN_TYPE="docker"
    else
        SCAN_TYPE="dir"
    fi
fi

# Detect app name if not specified
if [[ -z "$APP_NAME" ]]; then
    APP_NAME="$(basename "$REPO_DIR"):local"
fi

echo "Configuration:"
echo "  • Scan Type: $SCAN_TYPE"
echo "  • App / Image Tag: $APP_NAME"

# 1. Create target directories
mkdir -p "${REPO_DIR}/scripts"
mkdir -p "${REPO_DIR}/.github/workflows"

# 2. Copy scripts
echo -n "Installing local generator, analyzer, and test harness ... "
cp "${SKILL_ROOT}/scripts/generate_boms.sh" "${REPO_DIR}/scripts/generate_boms.sh"
cp "${SKILL_ROOT}/scripts/analyze_cbom.py" "${REPO_DIR}/scripts/analyze_cbom.py"
cp "${SKILL_ROOT}/scripts/test_boms.sh" "${REPO_DIR}/scripts/test_boms.sh"
chmod +x "${REPO_DIR}/scripts/generate_boms.sh" \
         "${REPO_DIR}/scripts/analyze_cbom.py" \
         "${REPO_DIR}/scripts/test_boms.sh"
echo "✅ Done"

# 3. Generate GitHub Actions Workflow
WORKFLOW_FILE="${REPO_DIR}/.github/workflows/sbom-cbom.yml"
echo -n "Installing GitHub Actions workflow with integrated test harness ... "

if [[ "$SCAN_TYPE" == "docker" ]]; then
    BUILD_STEP="
      - name: Build Docker Image
        run: docker build -t ${APP_NAME} .

      - name: Generate SBOM from Container Image
        uses: anchore/sbom-action@3ad7283483fc7af8ff2b4ea19663c2d5ca935e26 # v0.16.1
        with:
          image: ${APP_NAME}
          format: spdx-json
          output-file: oss/sbom.spdx.json

      - name: Generate CBOM from Container Image
        run: cdxgen -t docker --include-crypto -o oss/cbom.json ${APP_NAME}
"
else
    BUILD_STEP="
      - name: Generate SBOM from Repository Directory
        uses: anchore/sbom-action@3ad7283483fc7af8ff2b4ea19663c2d5ca935e26 # v0.16.1
        with:
          path: .
          format: spdx-json
          output-file: oss/sbom.spdx.json

      - name: Generate CBOM from Repository Directory
        run: cdxgen --include-crypto -o oss/cbom.json .
"
fi

cat <<EOF > "$WORKFLOW_FILE"
name: Generate and Verify SBOM & CBOM

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  generate-and-verify-boms:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Create output directory
        run: mkdir -p oss

      - name: Set up Node.js for cdxgen
        uses: actions/setup-node@v7
        with:
          node-version: '20'

      - name: Install cdxgen
        run: npm install -g @cyclonedx/cdxgen
${BUILD_STEP}
      # -------------------------------------------------------------
      # Automated Verification & Test Harness in CI
      # -------------------------------------------------------------
      - name: Run BOM Verification and Cryptographic Audit Harness
        run: bash scripts/test_boms.sh oss

      # -------------------------------------------------------------
      # Artifact Upload
      # -------------------------------------------------------------
      - name: Upload BOM Artifacts
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.3.3
        with:
          name: oss-boms
          path: oss/
          retention-days: 30
EOF
echo "✅ Done"

echo "=================================================================="
echo "🎉 Installation Complete!"
echo "Files installed:"
echo "  • ${REPO_DIR}/scripts/generate_boms.sh"
echo "  • ${REPO_DIR}/scripts/analyze_cbom.py"
echo "  • ${REPO_DIR}/scripts/test_boms.sh"
echo "  • ${REPO_DIR}/.github/workflows/sbom-cbom.yml"
echo ""
echo "To test locally inside ${REPO_DIR}:"
echo "  bash scripts/generate_boms.sh ${APP_NAME}"
echo "  bash scripts/test_boms.sh oss"
echo "=================================================================="
