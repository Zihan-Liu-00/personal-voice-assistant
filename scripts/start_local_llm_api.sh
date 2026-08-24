#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src"
exec /Users/zihanliu/Projects/.venv/bin/python -m personal_assistant.local_llm_api
