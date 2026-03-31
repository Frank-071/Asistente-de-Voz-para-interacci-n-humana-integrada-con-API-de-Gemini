import random

def reply(slots):
    # Usamos .get con un valor por defecto seguro
    query = (slots.get("texto") or "").lower().strip()
    
    # Lista de chistes para que no siempre diga el mismo
    chistes = [
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
        "¿Cuál es el colmo de un Alquimista? Que se le oxide el conocimiento."
        "¿Qué le dice un ganso a una gansa? ¡Vengansa!"
        "¡Camarero! Hay una mosca en mi sopa. No se preocupe, la araña que está en el pan se encargará de ella."
    ]

    if "chiste" in query:
        return random.choice(chistes)

    # Si el usuario solo dice "Hola" o algo genérico
    if any(w in query for w in ["hola", "buenos días", "buenas tardes"]):
        return "¡Hola Frank! Estoy lista para ayudarte. ¿Qué tienes en mente?"

    # Si no detecta nada específico, devolvemos None para que el core 
    # sepa que debe mandarlo a Gemini 2.0 Flash
    return None
