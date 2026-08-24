from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    llm_model: str = os.getenv('ASSISTANT_MODEL', '/Users/zihanliu/Projects/LLM/models/Qwen2.5-14B-4bit')
    asr_model: str = os.getenv('ASSISTANT_ASR_MODEL', 'mlx-community/whisper-small-mlx')
    language: str = os.getenv('ASSISTANT_LANGUAGE', 'zh')
    hotkey: str = '<ctrl>+<cmd>+z'
    sample_rate: int = 16000
    max_record_seconds: int = 300
    llm_max_tokens: int = 512

CONFIG = Config()
