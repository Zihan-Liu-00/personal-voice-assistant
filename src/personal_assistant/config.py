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
    tts_model: str = os.getenv('ASSISTANT_TTS_MODEL', '/Users/zihanliu/Projects/personal_voice_assistant/models/VoxCPM2')
    tts_device: str = os.getenv('ASSISTANT_TTS_DEVICE', 'auto')
    tts_timesteps: int = int(os.getenv('ASSISTANT_TTS_TIMESTEPS', '10'))
    tts_reference: str = os.getenv('ASSISTANT_TTS_REFERENCE', '/Users/zihanliu/Projects/personal_voice_assistant/reference/voice_reference.wav')
    # Conservative limit for the assembled prompt; compression happens before this is exceeded.
    context_safe_chars: int = int(os.getenv('ASSISTANT_CONTEXT_SAFE_CHARS', '24000'))
    context_keep_turns: int = int(os.getenv('ASSISTANT_CONTEXT_KEEP_TURNS', '10'))

CONFIG = Config()
