from __future__ import annotations
import subprocess

class TTS:
    """Fast local backend using macOS built-in speech; replaceable by a neural TTS later."""
    def __init__(self, voice='Ting-Ting', rate=190): self.voice=voice; self.rate=rate
    def speak(self, text):
        subprocess.run(['say','-v',self.voice,'-r',str(self.rate),text], check=False)
