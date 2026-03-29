# tts/sapi_tts.py
import win32com.client as win32

class SapiTTS:
    def __init__(self, voice_substring=None, rate=0, volume=100, device_substring=None):
        self.voice = win32.Dispatch("SAPI.SpVoice")

        # Voz (opcional)
        if voice_substring:
            for v in self.voice.GetVoices():
                if voice_substring.lower() in v.GetDescription().lower():
                    self.voice.Voice = v
                    break

        # 🔊 Dispositivo de salida (¡clave!)
        if device_substring:
            cat = win32.Dispatch("SAPI.SpObjectTokenCategory")
            cat.SetId(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\AudioOutput", False)
            for t in cat.EnumerateTokens():
                if device_substring.lower() in t.GetDescription().lower():
                    self.voice.AudioOutput = t
                    break

        self.voice.Rate = rate      # -10..10
        self.voice.Volume = volume  # 0..100

    def say(self, text, wait=True):
        flags = 0 if wait else 1  # 0 = sincrónico
        self.voice.Speak(str(text), flags)

    def close(self): 
        pass
