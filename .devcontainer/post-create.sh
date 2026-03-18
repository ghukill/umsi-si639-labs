#!/usr/bin/env bash
set -euo pipefail

# install uv
if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found; installing via astral.sh installer..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# setup virtual environment
uv venv .venv --python 3.12
uv sync

echo "UMSI-639 Labs DevContainer ready."