from __future__ import annotations
import tempfile, threading
from pathlib import Path
from pynput import keyboard
import soundfile as sf
from .config import CONFIG
from .audio import Recorder
from .asr import ASR
from .llm import LLM
from .tts import TTS
from .router import Router
from .google_tool import google_search
from .memory import MemoryService

class VoiceAssistant:
    def __init__(self):
        self.recorder=Recorder(CONFIG.sample_rate,CONFIG.max_record_seconds)
        self.asr=ASR(CONFIG.asr_model,CONFIG.language)
        self.llm=LLM(CONFIG.llm_model,CONFIG.llm_max_tokens)
        self.router=Router(self.llm)
        self.memory=MemoryService()
        self.tts=TTS(); self.busy=False

    def toggle(self):
        if self.busy: return
        if self.recorder.recording:
            audio=self.recorder.stop()
            if audio is not None: threading.Thread(target=self.process,args=(audio,),daemon=True).start()
            return
        self.recorder.start(); print('[录音中] 再按 Control+Command+Z 结束',flush=True)

    def process(self,audio):
        self.busy=True
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as f: path=f.name
            try:
                sf.write(path,audio,CONFIG.sample_rate); text=self.asr.transcribe(path)
                if not text: print('[未识别到语音]',flush=True); return
                print('[你] '+text,flush=True)
                route=self.router.route(text); print('[路由] '+str(route),flush=True)
                memory_context=self.memory.context(text)
                if route.get('need_web_search'):
                    query=route.get('query') or text; print('[联网搜索] '+query,flush=True)
                    results=google_search(query); answer=self.llm.chat(text,context=memory_context+'\n'+results)
                else:
                    answer=self.llm.chat(text,context=memory_context)
                saved=self.memory.capture_explicit(text)
                if saved: print('[记忆已保存] '+str(saved),flush=True)
                print('[助手] '+answer,flush=True); self.tts.speak(answer)
            finally: Path(path).unlink(missing_ok=True)
        except Exception as e: print('[错误] '+str(e),flush=True)
        finally: self.busy=False

def main():
    app=VoiceAssistant(); print('本地语音助手已启动：Control+Command+Z 开始/结束录音；Control+C 退出',flush=True)
    with keyboard.GlobalHotKeys({CONFIG.hotkey:app.toggle}) as listener: listener.join()
