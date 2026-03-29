# wake/simple_wake.py
class SimpleWake:
    def __init__(self, cfg):
        self.words = [w.lower() for w in cfg["wake_words"]]  # Asegúrate que "lila" esté aquí

    def triggered(self, text: str) -> bool:
        print(f"Escuché: {text}")  # Para depurar y ver lo que se está detectando
        t = text.lower()
        return any(w in t for w in self.words)  # Compara con las palabras clave configuradas