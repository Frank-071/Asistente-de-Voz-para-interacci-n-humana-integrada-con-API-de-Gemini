# nlu/sklearn_nlu.py
import re, unicodedata, joblib
from pathlib import Path

def norm(s: str) -> str:
    s = s.lower().strip()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

GAZETTEER_APPS = {
    "youtube":   ["youtube","you tube","yutube","yt","el youtube"],
    "chrome":    ["chrome","google chrome","navegador","gugle","googl"],
    "spotify":   ["spotify","spoty","spoti","música en spotify"],
    "whatsapp":  ["whatsapp","guasap","wasap","wasapp","wsp"],
    "gmail":     ["gmail","correo de google","gemail","correo gmail"],
    "calculadora":["calculadora","calc","la calculadora"],
    "word":      ["word","microsoft word","procesador de textos"],
    "excel":     ["excel","microsoft excel","hoja de cálculo","sheet"],
    "powerpoint":["powerpoint","power point","presentaciones"],
    "notepad":   ["bloc de notas","notepad","editor de texto simple","bloc"],
    "vscode":    ["vscode","visual studio code","code","editor de código"],
    "telegram":  ["telegram","telegran"],
    "facebook":  ["facebook","feis","face"],
    "tiktok":    ["tiktok","tik tok","tik-tok"],
    "steam":     ["steam","tienda de steam"],
    "google":    ["google","buscador","navegador google"]
}

# 🔒 Frases de salida de alta prioridad (puedes añadir más)
EXIT_PHRASES = [
    "salir","termina","terminar","apagate","apágate",
    "cerrar asistente","cierra asistente","apaga",
    "me voy","ya sal","apaga el asistente"
]

def has_phrase(text_norm: str, phrase_norm: str) -> bool:
    # palabra completa (evita que "sal" matchee "salsa")
    return re.search(rf"\b{re.escape(phrase_norm)}\b", text_norm) is not None

class SklearnNLU:
    def __init__(self, model_path="models/nlu_intents.joblib", threshold=0.35):
        self.model = joblib.load(model_path if isinstance(model_path, (str, Path)) else "models/nlu_intents.joblib")
        self.threshold = threshold

    def parse(self, text: str):
        txt = text or ""
        n = norm(txt)

        # ✅ Override: si detecta frase de salida → fuerza intent "salir"
        for p in EXIT_PHRASES:
            if has_phrase(n, norm(p)):
                return "salir", {}

        # --- ML para el resto ---
        intent = self.model.predict([txt])[0]
        proba  = float(max(self.model.predict_proba([txt])[0]))
        slots = {}

        # Slots por diccionario (rápido y robusto a faltas)
        for app, aliases in GAZETTEER_APPS.items():
            if any(norm(a) in n for a in aliases):
                slots["app"] = app
                break

        # Fallback si baja confianza
        if proba < self.threshold:
            intent = "smalltalk" if "hola" in n or "gracias" in n else "fallback"

        return intent, slots

