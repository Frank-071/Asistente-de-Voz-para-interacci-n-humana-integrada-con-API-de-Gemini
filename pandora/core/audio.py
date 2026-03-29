# core/audio.py
import winsound

def ding():
    winsound.Beep(880, 200)  # beep de 880 Hz durante 200 ms
