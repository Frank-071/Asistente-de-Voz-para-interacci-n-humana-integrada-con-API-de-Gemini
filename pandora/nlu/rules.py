# nlu/rules.py
import re

class RuleNLU:
    def parse(self, text: str):
        
        # FIX 1: Se agregó la regla para la hora que faltaba.
        # Busca frases como "qué hora es" o "dime la hora".
        if re.search(r'\b(qué hora es|dime la hora)\b', text, re.IGNORECASE):
            return "hora", {}

        # FIX 2: La variable 't' se cambió por 'text' y se añadió re.IGNORECASE.
        # Ahora reconocerá "Abre Spotify", "abre spotify", "Abrir Spotify", etc.
        m = re.search(r'\b(abre|abrir)\s+(youtube|google|gmail|spotify|calculadora)\b', text, re.IGNORECASE)
        if m:
            # Devuelve la intención "abrir" y la aplicación que reconoció.
            return "abrir", {"app": m.group(2).lower()} # .lower() para estandarizar

        # FIX 3: Corregido para 'buscar' y para aceptar frases más flexibles.
        m = re.search(r'\b(busca|buscar)\s+(.*)\s+en\s+(youtube|google)\b', text, re.IGNORECASE)
        if m:
            return "buscar", {"query": m.group(2), "destino": m.group(3).lower()}

        # FIX 4: Corregido para 'salir'.
        if re.search(r'\b(adiós|termina|salir|gracias eso es todo)\b', text, re.IGNORECASE):
            return "salir", {}

        # Si ninguna regla coincide, se devuelve una intención genérica de "charla".
        return "charla", {"texto": text}
