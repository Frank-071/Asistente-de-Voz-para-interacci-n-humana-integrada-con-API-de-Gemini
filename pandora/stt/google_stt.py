import speech_recognition as sr

class GoogleSTT:
    def __init__(self, cfg):
        self.r = sr.Recognizer()
        self.locale = cfg["locale"]
        self.timeout = cfg["mic"]["timeout"]
        self.phrase_time_limit = cfg["mic"]["phrase_time_limit"]
        self.adjust = cfg["mic"]["adjust_noise_sec"]

    def listen_short(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=self.adjust)
            # Ajustar para un mayor tiempo de espera si es necesario
            audio = self.r.listen(source, timeout=10, phrase_time_limit=5)
        try:
            return self.r.recognize_google(audio, language=self.locale)
        except Exception as e:
            print(f"Error: {e}")
            return ""


    def listen_command(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
            audio = self.r.listen(source, timeout=self.timeout, phrase_time_limit=self.phrase_time_limit)
        try:
            return self.r.recognize_google(audio, language=self.locale)
        except: return ""
