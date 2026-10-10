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
mkdir -p "${REPO_DIR}/docs/security"
mkdir -p "${REPO_DIR}/oss"

# 2. Copy scripts
echo -n "Installing local generator, analyzer, AST scanner, and test harness ... "
cp "${SKILL_ROOT}/scripts/generate_boms.sh" "${REPO_DIR}/scripts/generate_boms.sh"
cp "${SKILL_ROOT}/scripts/analyze_cbom.py" "${REPO_DIR}/scripts/analyze_cbom.py"
cp "${SKILL_ROOT}/scripts/scan_crypto_ast.py" "${REPO_DIR}/scripts/scan_crypto_ast.py"
cp "${SKILL_ROOT}/scripts/test_boms.sh" "${REPO_DIR}/scripts/test_boms.sh"
if [[ -f "${SKILL_ROOT}/scripts/known_cbom_catalog.json" ]]; then
    cp "${SKILL_ROOT}/scripts/known_cbom_catalog.json" "${REPO_DIR}/scripts/known_cbom_catalog.json"
fi
if [[ -f "${SKILL_ROOT}/scripts/fetch_oci_cbom.py" ]]; then
    cp "${SKILL_ROOT}/scripts/fetch_oci_cbom.py" "${REPO_DIR}/scripts/fetch_oci_cbom.py"
    chmod +x "${REPO_DIR}/scripts/fetch_oci_cbom.py"
fi
if [[ -f "${SKILL_ROOT}/scripts/attach_oci_bom.sh" ]]; then
    cp "${SKILL_ROOT}/scripts/attach_oci_bom.sh" "${REPO_DIR}/scripts/attach_oci_bom.sh"
    chmod +x "${REPO_DIR}/scripts/attach_oci_bom.sh"
fi
if [[ -f "${SKILL_ROOT}/scripts/enrich_sbom_gradle.py" && ( -f "${REPO_DIR}/build.gradle" || -f "${REPO_DIR}/build.gradle.kts" ) ]]; then
    cp "${SKILL_ROOT}/scripts/enrich_sbom_gradle.py" "${REPO_DIR}/scripts/enrich_sbom_gradle.py"
    chmod +x "${REPO_DIR}/scripts/enrich_sbom_gradle.py"
fi

chmod +x "${REPO_DIR}/scripts/generate_boms.sh" \
         "${REPO_DIR}/scripts/analyze_cbom.py" \
         "${REPO_DIR}/scripts/scan_crypto_ast.py" \
         "${REPO_DIR}/scripts/test_boms.sh"
echo "✅ Done"

# 3. Determine workflow filename
if [[ -f "${REPO_DIR}/.github/workflows/sbom.yml" ]]; then
    WORKFLOW_FILE="${REPO_DIR}/.github/workflows/sbom.yml"
elif [[ -f "${REPO_DIR}/.github/workflows/sbom-cbom.yml" ]]; then
    WORKFLOW_FILE="${REPO_DIR}/.github/workflows/sbom-cbom.yml"
else
    WORKFLOW_FILE="${REPO_DIR}/.github/workflows/sbom-cbom.yml"
fi

echo -n "Installing GitHub Actions workflow (${WORKFLOW_FILE}) ... "

GRADLE_SETUP=""
GRADLE_ENRICH=""
if [[ -f "${REPO_DIR}/build.gradle" || -f "${REPO_DIR}/build.gradle.kts" ]]; then
    GRADLE_SETUP="
      - name: Setup Java
        uses: actions/setup-java@de7274f081f381c8f8158605e0321c36c376e2e6 # v6.0.1
        with:
          java-version: '25'
          distribution: 'temurin'
          cache: 'gradle'
"
    GRADLE_ENRICH="
      - name: Enrich SBOM with Gradle Runtime Dependencies
        run: |
          if [ -f scripts/enrich_sbom_gradle.py ]; then
            python3 scripts/enrich_sbom_gradle.py oss/sbom.cyclonedx.json
          fi
"
fi

cat <<EOF > "$WORKFLOW_FILE"
name: Software & Cryptographic Bill of Materials (SBOM & CBOM)

on:
  push:
    branches:
      - main
      - master
    tags:
      - 'v*'
  pull_request:
    branches:
      - main
      - master
  workflow_dispatch:

permissions:
  contents: write
  id-token: write

jobs:
  generate-and-verify-boms:
    name: Generate, Verify, and Upload BOMs
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1 (Node 24)
        with:
          fetch-depth: 0

      - name: Create output directory
        run: mkdir -p oss
${GRADLE_SETUP}
      # -------------------------------------------------------------
      # 1. Generate SBOM (CycloneDX and SPDX via Anchore / Syft)
      # -------------------------------------------------------------
      - name: Generate CycloneDX SBOM (Anchore / Syft)
        uses: anchore/sbom-action@006b7ce8314066bdf1765b4500370d40fa6917a3 # v0.24.2
        with:
          path: .
          format: cyclonedx-json
          output-file: oss/sbom.cyclonedx.json
          upload-artifact: false
${GRADLE_ENRICH}
      - name: Generate SPDX SBOM (Anchore / Syft)
        uses: anchore/sbom-action@006b7ce8314066bdf1765b4500370d40fa6917a3 # v0.24.2
        with:
          path: .
          format: spdx-json
          output-file: oss/sbom.spdx.json
          upload-artifact: false

      # -------------------------------------------------------------
      # 2. Generate CBOM (cbomkit-action)
      # -------------------------------------------------------------
      - name: Generate Cryptographic Bill of Materials (CBOM)
        uses: cbomkit/cbomkit-action@34a3d960625ae7f7f1b59455eff93a96df090eb7 # v2.3.0
        id: cbom
        continue-on-error: true
        env:
          CBOMKIT_OUTPUT_DIR: oss
          CBOMKIT_EXCLUDE: "(^|/)scripts/.*|(^|/)tests/.*"

      - name: Fix permissions for container-generated artifacts
        run: sudo chown -R \$(id -u):\$(id -g) oss/ || true

      # -------------------------------------------------------------
      # 3. Dual-Engine Semantic AST Crypto Discovery & Reconciliation
      # -------------------------------------------------------------
      - name: Set up Python for Cryptographic Auditing
        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
        with:
          python-version: '3.11'

      - name: Semantic AST Cryptographic Scan & CBOM Reconciliation
        run: |
          if [ -f scripts/scan_crypto_ast.py ]; then
            python3 scripts/scan_crypto_ast.py . \\
              --cbom oss/cbom.json \\
              --output-json oss/crypto-callsites.json
          fi

      # -------------------------------------------------------------
      # 4. Automated Verification & Test Harness in CI
      # -------------------------------------------------------------
      - name: Run BOM Verification and Cryptographic Audit Harness
        run: |
          if [ -f scripts/test_boms.sh ]; then
            bash scripts/test_boms.sh oss
          fi

      # -------------------------------------------------------------
      # 5. Post-Quantum Cryptography (PQC) Readiness Assessment
      # -------------------------------------------------------------
      - name: Generate PQC Migration Dashboard & Step Summary
        run: |
          if [ -f scripts/analyze_cbom.py ]; then
            SBOM_ARG=""
            if [ -f oss/sbom.cyclonedx.json ]; then
              SBOM_ARG="--sbom oss/sbom.cyclonedx.json"
            elif [ -f oss/sbom.spdx.json ]; then
              SBOM_ARG="--sbom oss/sbom.spdx.json"
            fi
            EXT_ARG=""
            if [ -f oss/upstream_cbom.json ]; then
              EXT_ARG="--external-cbom oss/upstream_cbom.json"
            fi
            python3 scripts/analyze_cbom.py oss/cbom.json \\
              \$SBOM_ARG \\
              \$EXT_ARG \\
              --json oss/crypto-analysis.json \\
              --markdown oss/crypto-summary.md \\
              --step-summary
          fi

      # -------------------------------------------------------------
      # 6. Publish Cryptographic Audit Report to Repository (docs/security)
      # -------------------------------------------------------------
      - name: Publish Cryptographic Audit Report to Repository
        if: github.event_name == 'push' && !contains(github.event.head_commit.message, '[skip ci]')
        run: |
          if [ -f oss/crypto-summary.md ]; then
            mkdir -p docs/security
            cp oss/crypto-summary.md docs/security/CRYPTOGRAPHIC_AUDIT.md
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add docs/security/CRYPTOGRAPHIC_AUDIT.md
            if git diff --staged --quiet; then
              echo "No changes in cryptographic audit report."
            else
              git commit -m "docs(security): update cryptographic audit & PQC migration report [skip ci]"
              git push
            fi
          fi

      # -------------------------------------------------------------
      # 7. Upload All BOM Artifacts
      # -------------------------------------------------------------
      - name: Upload BOM Artifacts
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2
        with:
          name: bom-artifacts
          path: oss/
          retention-days: 90
EOF
echo "✅ Done"

# 4. Generate Initial Local Audit & Documentation
if [[ -f "${REPO_DIR}/oss/cbom.json" ]]; then
    echo -n "Generating local cryptographic scan and updating documentation ... "
    python3 "${REPO_DIR}/scripts/scan_crypto_ast.py" "${REPO_DIR}" --cbom "${REPO_DIR}/oss/cbom.json" >/dev/null 2>&1 || true
    python3 "${REPO_DIR}/scripts/analyze_cbom.py" "${REPO_DIR}/oss/cbom.json" --markdown "${REPO_DIR}/oss/crypto-summary.md" >/dev/null 2>&1 || true
    if [[ -f "${REPO_DIR}/oss/crypto-summary.md" ]]; then
        cp "${REPO_DIR}/oss/crypto-summary.md" "${REPO_DIR}/docs/security/CRYPTOGRAPHIC_AUDIT.md"
    fi
    echo "✅ Done"
else
    echo "Skipping initial audit: No CBOM detected. Please run 'bash scripts/generate_boms.sh' first to populate the oss/ directory."
fi
echo "✅ Done"

echo "=================================================================="
echo "🎉 Installation Complete for ${REPO_DIR}!"
echo "=================================================================="
