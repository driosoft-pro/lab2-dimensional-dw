#!/usr/bin/env bash
###############################################################
# clean.sh — Remove generated files
###############################################################
set -euo pipefail

echo "Cleaning generated files..."

rm -rf .venv
rm -rf database/retail_dw.db
rm -f docs/visualization_monthly_sales.png
rm -f docs/visualization_sales_by_store.png
rm -rf src/__pycache__

echo "Done."
