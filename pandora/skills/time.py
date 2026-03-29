# skills/time.py
from datetime import datetime

# AÑADE 'slots' AQUÍ
def say_time(slots):
    # Formato de 12 horas (AM/PM). Ej: "01:30 PM"
    hora_actual = datetime.now().strftime("%I:%M %p")
    return f"Son las {hora_actual}."
