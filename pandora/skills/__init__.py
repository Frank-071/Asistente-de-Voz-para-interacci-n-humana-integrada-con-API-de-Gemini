# skills/__init__.py

# 1. Importa las funciones de cada archivo de skill
from .time import say_time
from .open_app import open_app
# from .search import search_stuff  <-- Descomenta cuando la crees
# from .smalltalk import talk      <-- Descomenta cuando la crees

# 2. Crea el diccionario que mapea la intención a la función
SKILLS = {
    "hora": say_time,
    "abrir": open_app,
    # "buscar": search_stuff,
    # "charla": talk
}