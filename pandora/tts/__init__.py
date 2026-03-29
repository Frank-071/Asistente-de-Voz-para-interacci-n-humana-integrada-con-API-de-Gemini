# tts/__init__.py
from typing import Any, Dict

def build_tts(cfg: Dict[str, Any]):
    backend = (cfg.get("tts_backend") or "sapi").lower()
    if backend == "sapi":
        from .sapi_tts import SapiTTS
        return SapiTTS(
            voice_substring=cfg.get("tts_voice"),
            rate=int(cfg.get("tts_rate", 0)),
            volume=int(cfg.get("tts_volume", 100)),
            device_substring=cfg.get("tts_device"),
        )
    else:
        from .pyttsx3_tts import Pyttsx3TTS
        return Pyttsx3TTS(
            voice=cfg.get("tts_voice"),
            rate=int(cfg.get("tts_rate", 180)),
            volume=float(cfg.get("tts_volume", 1.0)),
        )
