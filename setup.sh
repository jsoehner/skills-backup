#!/usr/bin/env bash
# ==============================================================================
# Setup script for Skills Backup repository (Bash)
# Restores agent skills, displays the skills catalog, and inspects status.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESTORE_SCRIPT="$SCRIPT_DIR/scripts/restore_skills.py"
CATALOG_SCRIPT="$SCRIPT_DIR/scripts/catalog.py"

# Default configuration
CLIENT="pi"
ACTION="restore"
CATEGORY=""
SEARCH_QUERY=""
EXTRA_ARGS=()

print_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [-- EXTRA_ARGS]

Setup and manage agent skills for your local AI runtime clients.

Options:
  -c, --client CLIENT      Target AI client: pi, gemini, claude, opencode (default: pi)
  -C, --catalog            Display skills catalog grouped by category
  -s, --status             Show installation status (existing vs new skills) for target client
      --new                Show only new/uninstalled skills for target client
      --installed          Show only existing/installed skills for target client
      --categories         List all available skill categories with counts
  -m, --memory             Show local memory & RAG system architecture and host status
  -g, --category NAME      Filter catalog or status by category name
  -q, --search QUERY       Search skills by name or description keyword
  -r, --restore            Restore skills to the target client (default action)
  -h, --help               Show this help message and exit

Examples:
  ./setup.sh --client gemini              # Restore skills to Gemini
  ./setup.sh --status --client gemini     # Show new vs existing skills for Gemini
  ./setup.sh --new --client claude        # List new skills not yet in Claude
  ./setup.sh --catalog                    # Display complete skills catalog
  ./setup.sh --catalog -g databases_data  # View database category skills
  ./setup.sh --catalog -q postgres        # Search catalog for 'postgres'
  ./setup.sh --categories                 # List categories and counts
  ./setup.sh --memory                     # Inspect local memory system (OKF + ChromaDB)
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--client)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --client requires an argument (pi, gemini, claude, opencode)." >&2
                exit 1
            fi
            CLIENT="$2"
            shift 2
            ;;
        -C|--catalog)
            ACTION="catalog"
            shift
            ;;
        -s|--status)
            ACTION="status"
            shift
            ;;
        --new)
            ACTION="new"
            shift
            ;;
        --installed|--existing)
            ACTION="installed"
            shift
            ;;
        --categories)
            ACTION="categories"
            shift
            ;;
        -m|--memory|--memory-info)
            ACTION="memory"
            shift
            ;;
        -g|--group|--category)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --category requires a category name." >&2
                exit 1
            fi
            CATEGORY="$2"
            shift 2
            ;;
        -q|--search)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --search requires a search query." >&2
                exit 1
            fi
            SEARCH_QUERY="$2"
            shift 2
            ;;
        -r|--restore)
            ACTION="restore"
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        --)
            shift
            EXTRA_ARGS+=("$@")
            break
            ;;
        *)
            EXTRA_ARGS+=("$1")
            shift
            ;;
    esac
done

# Validate client choice
case "$CLIENT" in
    pi|gemini|claude|opencode)
        ;;
    *)
        echo "Error: Invalid client '$CLIENT'. Supported clients: pi, gemini, claude, opencode." >&2
        exit 1
        ;;
esac

# Locate Python 3 interpreter
PYTHON_BIN=""
for cmd in python3 python py; do
    if command -v "$cmd" >/dev/null 2>&1; then
        if "$cmd" -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)" >/dev/null 2>&1; then
            PYTHON_BIN="$cmd"
            break
        fi
    fi
done

if [[ -z "$PYTHON_BIN" ]]; then
    echo "Error: Python 3 (version 3.7+) is required but was not found in PATH." >&2
    exit 1
fi

# Route based on action
if [[ "$ACTION" == "restore" ]]; then
    if [[ ! -f "$RESTORE_SCRIPT" ]]; then
        echo "Error: Restore script not found at '$RESTORE_SCRIPT'." >&2
        exit 1
    fi

    echo "=================================================="
    echo "Skills Backup Setup"
    echo "=================================================="
    echo "Repository Root : $SCRIPT_DIR"
    echo "Target Client   : $CLIENT"
    echo "Python Runtime  : $("$PYTHON_BIN" --version 2>&1)"
    echo "=================================================="
    echo ""

    if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
        "$PYTHON_BIN" "$RESTORE_SCRIPT" "$SCRIPT_DIR" --client "$CLIENT" "${EXTRA_ARGS[@]}"
    else
        "$PYTHON_BIN" "$RESTORE_SCRIPT" "$SCRIPT_DIR" --client "$CLIENT"
    fi

    echo ""
    echo "Setup complete!"
else
    if [[ ! -f "$CATALOG_SCRIPT" ]]; then
        echo "Error: Catalog script not found at '$CATALOG_SCRIPT'." >&2
        exit 1
    fi

    CAT_CMD=("$PYTHON_BIN" "$CATALOG_SCRIPT" "--client" "$CLIENT")

    case "$ACTION" in
        catalog)
            CAT_CMD+=("--catalog")
            ;;
        status)
            CAT_CMD+=("--status")
            ;;
        new)
            CAT_CMD+=("--new")
            ;;
        installed)
            CAT_CMD+=("--installed")
            ;;
        categories)
            CAT_CMD+=("--categories")
            ;;
        memory)
            CAT_CMD+=("--memory")
            ;;
    esac

    if [[ -n "$CATEGORY" ]]; then
        CAT_CMD+=("--category" "$CATEGORY")
    fi

    if [[ -n "$SEARCH_QUERY" ]]; then
        CAT_CMD+=("--search" "$SEARCH_QUERY")
    fi

    if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
        "${CAT_CMD[@]}" "${EXTRA_ARGS[@]}"
    else
        "${CAT_CMD[@]}"
    fi
fi
