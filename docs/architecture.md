# Architecture

The current minimal runtime is a modular monolith:

`hotkey -> audio recorder -> ASR -> intent router -> memory/search -> (Google Browser Use) -> LLM -> memory/write -> macOS TTS`

The router only asks local Qwen whether web search is needed. Browser Use opens Google through deterministic code; Qwen does not control individual browser clicks. Memory uses SQLite and keyword retrieval only; transient questions such as weather are not stored. Model adapters and repositories are isolated so ASR, LLM, TTS and memory backends can be replaced independently.
