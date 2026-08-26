#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/src"
export ASSISTANT_TTS_REFERENCE="$PWD/reference/voice_reference.wav"
exec /Users/zihanliu/Projects/.venv/bin/python -m personal_assistant
