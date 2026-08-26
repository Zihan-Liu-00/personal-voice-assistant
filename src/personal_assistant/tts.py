from __future__ import annotations
import subprocess
import tempfile
from pathlib import Path
import soundfile as sf

class TTS:
    """Local VoxCPM 2.0 speech synthesis with ephemeral audio files."""
    def __init__(self, model_id='openbmb/VoxCPM2', device='auto', timesteps=10, reference=''):
        self.model_id=model_id; self.device=device; self.timesteps=timesteps; self.reference=reference; self.model=None; self.reference_cache=None
    def load(self):
        if self.model is None:
            from voxcpm import VoxCPM
            self.model=VoxCPM.from_pretrained(self.model_id, device=self.device, load_denoiser=False)
            if self.reference:
                print('[TTS] 正在预加载参考音频...',flush=True)
                self.reference_cache=self.model.tts_model.build_prompt_cache(reference_wav_path=self.reference)
                print('[TTS] 参考音频 cache 已就绪',flush=True)
    def speak(self, text):
        if not text or not text.strip(): return
        self.load()
        if self.reference_cache is not None and hasattr(self.model.tts_model,'_generate_with_prompt_cache'):
            stream=self.model.tts_model._generate_with_prompt_cache(
                target_text=text, prompt_cache=self.reference_cache,
                cfg_value=2.0, inference_timesteps=self.timesteps,
                retry_badcase=True,
            )
            try:
                wav=next(stream)[0].squeeze(0).cpu().numpy()
            finally:
                stream.close()
        else:
            kwargs={'text':text, 'cfg_value':2.0, 'inference_timesteps':self.timesteps}
            if self.reference: kwargs['reference_wav_path']=self.reference
            wav=self.model.generate(**kwargs)
        path=None
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f: path=Path(f.name)
            sf.write(path,wav,self.model.tts_model.sample_rate)
            subprocess.run(['afplay',str(path)],check=False)
        finally:
            if path: path.unlink(missing_ok=True)
