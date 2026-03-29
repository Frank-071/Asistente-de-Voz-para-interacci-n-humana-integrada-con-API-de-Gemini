import google.genai as genai
from core.config import load_config
from datetime import datetime

_cfg = load_config("config.yml")

# Opción A: Inicialización global (si quieres mantenerla fuera)
# Asegúrate de que el nombre coincida exactamente con tu config.yml
api_key = _cfg["google_ai"]["api_key"]
client = genai.Client(api_key=api_key)

def ask_llm(text: str) -> str:
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    # Instrucción de sistema para que sea directa y sencilla
    instruccion = (
        "Eres Pandora, una asistente eficiente. "
        "Tus respuestas deben ser breves, sencillas y sin explicar tus cálculos. "
        f"Hoy es {fecha_actual}."
    )
    
    try:
        # Enviamos la instrucción y la pregunta
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[instruccion, text] 
        )
        return response.text.strip()
    except Exception as e:
        print(f"DEBUG - Error: {e}")
        return "Error de conexión."
