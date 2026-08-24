from __future__ import annotations
import mlx_whisper

class ASR:
    def __init__(self, model, language='zh'):
        self.model=model; self.language=language

    def transcribe(self, audio_path):
        result=mlx_whisper.transcribe(audio_path, path_or_hf_repo=self.model, language=self.language, temperature=0.0, verbose=False)
        return result.get('text','').strip()
