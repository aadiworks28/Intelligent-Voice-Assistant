import pyttsx3
import simpleaudio as sa
import time
import os

SOUND_WAKE = "app/sounds/wake_beep.wav"
SOUND_END = "app/sounds/end_beep.wav"

def play_wake_sound():
    if os.path.exists(SOUND_WAKE):
        sa.WaveObject.from_wave_file(SOUND_WAKE).play()

def play_end_sound():
    if os.path.exists(SOUND_END):
        sa.WaveObject.from_wave_file(SOUND_END).play()

def speak(text, pitch=1.0, rate=170, pause=0.0):
    print(f"Assistant: {text}")

    engine = pyttsx3.init(driverName="nsss")

    # Select Samantha
    for v in engine.getProperty('voices'):
        if "samantha" in v.id.lower():
            engine.setProperty('voice', v.id)
            break

    engine.setProperty("rate", rate)

    time.sleep(pause)
    engine.say(text)
    engine.runAndWait()

