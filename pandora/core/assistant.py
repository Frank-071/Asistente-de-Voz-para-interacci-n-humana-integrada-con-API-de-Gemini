from core.audio import ding
from core.llm import ask_llm 

class Assistant:
    def __init__(self, cfg, stt, tts, wake, nlu, skills, llm_fallback=None):
        self.cfg, self.stt, self.tts, self.wake, self.nlu, self.skills = cfg, stt, tts, wake, nlu, skills
        self.llm_fallback = llm_fallback 
        self.name = cfg["assistant_name"]

    def run(self):
        self.tts.say(f"Di '{self.name}' para activarme.", wait=True)
        print(f"--- Di '{self.name}' para activarme. ---")

        while True:
            print(f"\n✅ ...esperando '{self.name}'...")
            try:
                # Intentamos escuchar
                text = self.stt.listen_short()
            except Exception: 
                # Si hay silencio total (Timeout), simplemente volvemos al inicio del while
                continue
            if not self.wake.triggered(text): 
                continue

            print(f"🟢 ¡'{self.name}' detectado!")
            ding() 
            
            user = text.lower().replace(self.name.lower(), "", 1).strip()
            user_lower = user.lower()
            print(f"🗣️  Comando extraído: '{user}'")

            if not user:
                self.tts.say("Dime, ¿cómo puedo ayudarte?", wait=True)
                continue
            
            try:
                intent, slots = self.nlu.parse(user)
                app_target = slots.get("app")

                # --- 1. CORRECCIÓN MANUAL DE INTENCIONES ---
                # Si dice "cierra", forzamos la intención 'cerrar'
                if any(w in user_lower for w in ["cierra", "cerrar", "quitar"]):
                    intent = "cerrar"
                    if not app_target:
                        app_target = user_lower.replace("cierra", "").replace("cerrar", "").strip()
                        slots["app"] = app_target

                # --- 2. FILTRO INTELIGENTE (EL SALVAVIDAS) ---
                # Si el NLU dice 'abrir' o 'buscar' pero no hay una app/tema, o es una pregunta clara
                es_pregunta = any(w in user_lower for w in ["quién", "qué", "cuánto", "cuántos", "cuándo", "cómo", "años", "presidente"])
                
                # Si la intención es abrir pero no hay App detectada, es casi seguro que es una pregunta para Gemini
                if intent in ["abrir", "buscar", "charla"] and not app_target:
                    intent = "gemini_fallback"
                
                if es_pregunta:
                    intent = "gemini_fallback"

                print(f"🧠  Intención Final: '{intent}' | App: {app_target}")
                
                reply = None
                if intent == "salir":
                    self.tts.say("Hasta luego, Frank.", wait=True)
                    break

                handler = self.skills.get(intent)
                
                # --- 3. EJECUCIÓN ---
                if handler and intent != "gemini_fallback": 
                    print(f"🚀  Ejecutando skill local: {intent}")
                    reply = handler(slots)
                    # Si la skill local dice que no encontró la app, probamos Gemini por si acaso
                    if "No tengo esa aplicación" in str(reply):
                        print("🔄 Skill falló, reintentando con Gemini...")
                        reply = self.llm_fallback(user)
                else:
                    print("🤖  Consultando a Gemini 2.0 Flash...")
                    reply = self.llm_fallback(user) 

                # --- 4. RESPUESTA ---
                if reply:
                    print(f"💬  Respuesta: '{reply}'")
                    self.tts.say(reply, wait=True) 

            except Exception as e:
                print(f"\n🚨  ERROR: {e}\n")
                self.tts.say("Hubo un error interno.")
