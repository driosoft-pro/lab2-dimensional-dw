#!/usr/bin/env bash
###############################################################
# setup.sh — Initial project setup
# Creates .venv via uv and installs dependencies
###############################################################
set -euo pipefail

echo "Setting up environment..."

if [ ! -d .venv ]; then
    echo "Creating virtual environment with uv..."
    uv venv --system-site-packages
fi

source .venv/bin/activate

echo "Installing dependencies from requirements.txt..."
uv pip install -r requirements.txt

echo ""
echo "Setup complete. Run './run.sh' to execute the pipeline."
