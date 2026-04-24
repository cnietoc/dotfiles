#!/usr/bin/env bash

set -euo pipefail

echo "Setting up atuin history sync..."

if ! command -v atuin &>/dev/null; then
  echo "atuin not found. Run: brew install atuin" >&2
  exit 1
fi

dot atuin setup

echo "Importing existing zsh history into atuin..."
atuin import zsh

echo "atuin setup complete."
