# tts/pyttsx3_tts.py
import pyttsx3
import threading
from typing import Optional

class Pyttsx3TTS:
    def __init__(self, voice: Optional[str] = None, rate: int = 180, volume: float = 1.0):
        self._voice_spec = voice
        self._rate = rate
        self._volume = volume
        self._lock = threading.Lock()
        self._init_engine()

    def _init_engine(self):
        # En Windows usa SAPI5 explícitamente
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty("rate", self._rate)
        self.engine.setProperty("volume", self._volume)
        if self._voice_spec:
            try:
                for v in self.engine.getProperty("voices"):
                    name_id = f"{v.name}||{v.id}".lower()
                    if self._voice_spec.lower() in name_id:
                        self.engine.setProperty("voice", v.id)
                        break
            except Exception:
                pass

    def say(self, text: str, wait: bool = True):
        if not text:
            return
        with self._lock:
            try:
                self.engine.stop()
            except Exception:
                pass

            msg = str(text)
            print(f"[TTS] BEGIN: {msg[:60]}{'...' if len(msg) > 60 else ''} | wait={wait}")
            self.engine.say(msg)
            if wait:
                try:
                    self.engine.runAndWait()
                    print("[TTS] END OK")
                except Exception as e:  # <<-- más amplio que RuntimeError
                    print("[TTS] ERROR en runAndWait(), reiniciando engine:", repr(e))
                    try:
                        self._init_engine()
                        self.engine.say(msg)
                        self.engine.runAndWait()
                        print("[TTS] END OK tras reinicio")
                    except Exception as e2:
                        print("[TTS] Error irrecuperable:", repr(e2))
            else:
                threading.Thread(target=self._run_async, daemon=True).start()

    def _run_async(self):
        try:
            self.engine.runAndWait()
        except Exception as e:
            print("[TTS] Error en ejecución asíncrona:", e)

    def close(self):
        with self._lock:
            try:
                self.engine.stop()
            except Exception:
                pass



