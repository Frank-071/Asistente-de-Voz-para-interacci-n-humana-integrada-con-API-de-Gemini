import sys
import os                           # <--- 1. Importamos os
from dotenv import load_dotenv      # <--- 2. Importamos dotenv

load_dotenv()
from core.config import load_config
from core.assistant import Assistant
from core.llm import ask_llm  # <--- Importamos tu nuevo cerebro
from stt.google_stt import GoogleSTT
from tts import build_tts
from wake.simple_wake import SimpleWake
from nlu.sklearn_nlu import SklearnNLU
from skills import time, open_app, search, smalltalk

if __name__ == "__main__":
    cfg = load_config("config.yml")
    
    # Inicialización de componentes
    stt = GoogleSTT(cfg)
    tts = build_tts(cfg)
    wake = SimpleWake(cfg)
    
    # Intentamos cargar el modelo NLU para comandos rápidos
    try:
        nlu = SklearnNLU("models/nlu_intents.joblib")
    except:
        from nlu.rules import RuleNLU
        nlu = RuleNLU()
        print("[DEBUG] Usando RuleNLU como respaldo.")

    # Diccionario de habilidades (Skills)
    # --- CONFIGURACIÓN DE HABILIDADES ---
    skills = {
        # Si la función existe la asigna, si no, usa una función lambda que no rompe el código
        "hora": getattr(time, 'say_time', lambda _: "No puedo dar la hora en este momento."),
        
        # Manejo dinámico para 'abrir': verifica si es el módulo o la función
        "abrir": open_app.open_app if hasattr(open_app, 'open_app') else open_app, 
        
        "buscar": getattr(search, 'search_web', lambda _: "La búsqueda no está disponible."),
        
        # Charla: si falla, devolverá None y activará automáticamente a Gemini
        "charla": getattr(smalltalk, 'reply', lambda _: None),
        
        # Salir: sys.exit es estándar, pero lo envolvemos por seguridad
        "salir": sys.exit
    }

    print(f"[DEBUG] TTS activo con: {cfg['tts_backend']}")
    tts.say("Hola Frank, soy Pandora. Estoy lista.", wait=True)

    # Creamos el asistente
    # IMPORTANTE: Asegúrate de que tu clase Assistant tenga soporte para fallback a LLM
    pandora = Assistant(cfg, stt, tts, wake, nlu, skills, llm_fallback=ask_llm)
    
    print(">>> Pandora escuchando... Di 'Hey Pandora' o tu palabra de activación.")
    pandora.run()
