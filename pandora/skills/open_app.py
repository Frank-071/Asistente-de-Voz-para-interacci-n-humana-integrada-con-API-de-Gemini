import webbrowser, platform, subprocess, os

def open_app(slots):
    app = slots.get("app","")
    if app == "youtube":
        webbrowser.open("https://youtube.com"); return "Abriendo YouTube."
    if app == "google":
        webbrowser.open("https://google.com"); return "Abriendo Google."
    if app == "gmail":
        webbrowser.open("https://mail.google.com"); return "Abriendo Gmail."
    if app == "spotify":
        webbrowser.open("https://open.spotify.com"); return "Abriendo Spotify."
    if app == "calculadora" and platform.system()=="Windows":
        subprocess.Popen("calc.exe"); return "Listo, calculadora abierta."
    if app == "whatsapp":
        if platform.system() == "Windows":
            # Este comando simula que escribes 'whatsapp' en el menú inicio y das Enter
            os.system("start whatsapp:") 
            return "Listo, abriendo WhatsApp."
    return "No tengo esa aplicación configurada."
