from __future__ import annotations
import threading, time
import numpy as np
import sounddevice as sd

class Recorder:
    def __init__(self, sample_rate=16000, max_seconds=300):
        self.rate=sample_rate; self.max_seconds=max_seconds; self.lock=threading.Lock()
        self.recording=False; self.started=0.0; self.stream=None; self.chunks=[]

    def start(self):
        with self.lock:
            if self.recording: return False
            self.chunks=[]; self.started=time.time(); self.recording=True
            self.stream=sd.InputStream(samplerate=self.rate, channels=1, dtype='float32', callback=self._callback)
            self.stream.start(); return True

    def _callback(self, indata, frames, timing, status):
        with self.lock:
            if self.recording: self.chunks.append(indata.copy())
            if self.recording and time.time()-self.started >= self.max_seconds:
                threading.Thread(target=self.stop, daemon=True).start()

    def stop(self):
        with self.lock:
            if not self.recording: return None
            self.recording=False; stream=self.stream; self.stream=None; chunks=self.chunks[:]; self.chunks=[]
        if stream: stream.stop(); stream.close()
        return np.concatenate(chunks,axis=0) if chunks else None
