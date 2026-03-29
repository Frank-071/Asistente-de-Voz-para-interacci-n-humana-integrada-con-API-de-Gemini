# skills/search.py
import webbrowser

def search_web(slots):
    # Obtenemos lo que el usuario quiere buscar de los 'slots'
    query = slots.get("query")
    destino = slots.get("destino", "google").lower()

    if not query:
        return "No entendí qué quieres buscar."

    # Creamos la URL de búsqueda
    if destino == "youtube":
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    else: # Por defecto, busca en Google
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    # Abrimos el navegador con la búsqueda
    webbrowser.open(url)
    
    return f"Buscando '{query}' en {destino}."
