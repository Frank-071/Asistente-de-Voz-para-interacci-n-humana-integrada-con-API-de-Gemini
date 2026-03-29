import sys
sys.stdout.reconfigure(encoding="utf-8")

from core.llm import ask_llm

if __name__ == "__main__":
    respuesta = ask_llm("¿Cuándo es el mundial del 2026, dime la fecha exacta?")
    print(respuesta)


