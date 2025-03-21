#!/usr/bin/env bash
set -e

echo "Installing pre-commit hooks using Poetry..."
# Ensure pre-commit is installed in your Poetry environment
poetry run pre-commit install
echo "Pre-commit hooks installed successfully."
