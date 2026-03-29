import os

def close_app(slots):
    # 'slots' debería contener el nombre de la app, ej: "chrome" o "notepad"
    app_name = slots.get("app") 
    
    if not app_name:
        return "No me dijiste qué aplicación cerrar."

    # Diccionario de traducción (lo que el usuario dice vs el proceso real)
    apps = {
        "navegador": "chrome.exe",
        "google chrome": "chrome.exe",
        "bloc de notas": "notepad.exe",
        "whatsapp": "WhatsApp.exe",  # Agregamos WhatsApp
        "spotify": "Spotify.exe",    # Agregamos Spotify
        "calculadora": "CalculatorApp.exe",
        "word": "winword.exe"
    }

    proceso = apps.get(app_name.lower(), f"{app_name}.exe")
    
    try:
        # Ejecuta el comando de Windows para cerrar procesos
        os.system(f"taskkill /f /im {proceso}")
        return f"He cerrado {app_name}."
    except Exception as e:
        return f"No pude cerrar {app_name}. ¿Seguro que está abierta?"