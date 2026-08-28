#!/usr/bin/env bash
###############################################################
# run.sh — Run the ETL Pipeline
# Usage: ./run.sh [--full | --schema | --load | --queries | --viz]
###############################################################
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"

usage() {
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  --full       Run the full pipeline (default)"
    echo "  --schema     Create schema only"
    echo "  --load       Load dimensions + facts only"
    echo "  --queries    Run analytical queries only"
    echo "  --viz        Generate visualizations only"
    echo "  --help       Show this help"
    exit 0
}

run_full() {
    echo "Running full ETL pipeline..."
    python "$SRC_DIR/main.py"
}

run_schema() {
    echo "Creating schema..."
    python "$SRC_DIR/create_schema.py"
}

run_load() {
    echo "Loading dimensions..."
    python "$SRC_DIR/load_dimensions.py"
    echo "Loading fact table..."
    python "$SRC_DIR/load_fact.py"
}

run_queries() {
    echo "Running analytical queries..."
    python "$SRC_DIR/queries.py"
}

run_viz() {
    echo "Generating visualizations..."
    python "$SRC_DIR/visualization.py"
}

case "${1:---full}" in
    --full)     run_full ;;
    --schema)   run_schema ;;
    --load)     run_load ;;
    --queries)  run_queries ;;
    --viz)      run_viz ;;
    --help|-h)  usage ;;
    *)          echo "Unknown option: $1"; usage ;;
esac
