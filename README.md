# Personal Voice Assistant

Local-first voice assistant for Apple Silicon.

## Runtime

`Control+Command+Z` → record → MLX Whisper ASR → Qwen LLM → macOS `say` TTS.

Start it with:

```bash
./start_assistant.sh
```

`start_hotkey_asr.sh` remains as a compatibility alias. Memory is stored locally in `data/memory.sqlite3` using SQLite and keyword retrieval; it is intentionally excluded from Git.

## Models and dependencies

- LLM: Qwen2.5-14B-4bit in MLX format. Set `ASSISTANT_MODEL` to its local path.
- ASR: `mlx-community/whisper-small-mlx`.
- Runtime: Python 3.13, MLX, mlx-whisper, sounddevice, soundfile, pynput, Browser Use.
- TTS: macOS built-in `say` command.

## Start

```bash
./start_assistant.sh
```

Press `Control+Command+Z` once to start recording and again to stop. The recognized text is routed to the local Qwen model, optionally searched through Google with Browser Use, and spoken with macOS TTS.

Grant Microphone and Accessibility permissions to the host application that starts the script (VS Code or Terminal).

## Project layout

```text
src/personal_assistant/audio.py       microphone recording
src/personal_assistant/asr.py         MLX Whisper ASR
src/personal_assistant/llm.py         local Qwen inference
src/personal_assistant/router.py      web-search intent routing
src/personal_assistant/google_tool.py deterministic Google search
src/personal_assistant/memory/        SQLite memory and keyword retrieval
src/personal_assistant/tts.py         macOS speech output
```
