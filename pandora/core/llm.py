import google.genai as genai
import os
from core.config import load_config
from datetime import datetime

_cfg = load_config("config.yml")

# Opción A: Inicialización global (si quieres mantenerla fuera)
# Asegúrate de que el nombre coincida exactamente con tu config.yml
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def ask_llm(text: str) -> str:
    # Agregamos también la hora para darle más contexto a Pandora
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%I:%M %p")
    
    # Instrucciones avanzadas para un asistente de voz
    instruccion = f"""Eres Pandora, una asistente de voz inteligente, amable y con personalidad propia. 
    
    Reglas estrictas para tus respuestas:
    1. TUS RESPUESTAS SERÁN LEÍDAS EN VOZ ALTA. NUNCA uses formato Markdown (nada de asteriscos **, viñetas -, o hashtags #). Escribe solo texto plano.
    2. Sé extremadamente concisa y conversacional. Responde en 1 o 2 oraciones como máximo. Ve directo al grano.
    3. Habla con naturalidad. Nunca uses frases robóticas como "Como modelo de lenguaje artificial..." o "Aquí tienes la respuesta...".
    4. Si te hacen una pregunta matemática o lógica, da la respuesta final directamente sin explicar el paso a paso.
    5. No saludes cada vez que hablas, asume que ya estamos en medio de una conversación.
    
    Contexto: Hoy es {fecha_actual} y son las {hora_actual}.
    """
    
    try:
        # Usamos System Instructions de forma nativa en la API (es más efectivo)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=text,
            config=genai.types.GenerateContentConfig(
                system_instruction=instruccion,
                temperature=0.7 # Un toque de creatividad sin perder precisión
            )
        )
        # La respuesta ya viene limpia sin formato Markdown, gracias a las instrucciones del sistema
        return response.text.strip()
    except Exception as e:
        print(f"DEBUG - Error de Gemini: {e}")
        return "Lo siento, tengo problemas para conectarme en este momento."
