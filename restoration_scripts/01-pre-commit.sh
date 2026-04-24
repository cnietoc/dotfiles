#!/usr/bin/env bash

set -euo pipefail

echo "Installing pre-commit hooks..."

if ! command -v pre-commit &>/dev/null; then
  echo "pre-commit not found. Run: brew install pre-commit" >&2
  exit 1
fi

pre-commit install --install-hooks

echo "pre-commit hooks installed."
