import simpleaudio as sa

def play_sound(path):
    try:
        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        return play_obj
    except Exception as e:
        print(f"[Sound Error] {e}")

def play_wake_sound():
    play_sound("sounds/wake.wav")

def play_end_sound():
    play_sound("sounds/end.wav")

