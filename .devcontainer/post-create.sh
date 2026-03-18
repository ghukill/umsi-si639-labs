#!/usr/bin/env bash
set -euo pipefail

uv venv .venv --python 3.12
uv sync

echo "UMSI-639 Labs DevContainer ready."