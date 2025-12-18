import os
import time

# -------------------------
# Sound file paths
# -------------------------
SOUND_WAKE = "app/sounds/wake_beep.wav"
SOUND_END = "app/sounds/end_beep.wav"


# -------------------------
# 1. Play wake sound
# -------------------------
def play_wake_sound():
    if os.path.exists(SOUND_WAKE):
        os.system(f"afplay '{SOUND_WAKE}' &")   # non-blocking
    else:
        print("[Warning] Wake beep not found.")


# -------------------------
# 2. Play end sound
# -------------------------
def play_end_sound():
    if os.path.exists(SOUND_END):
        os.system(f"afplay '{SOUND_END}' &")
    else:
        print("[Warning] End beep not found.")


# -------------------------
# 3. Speak using macOS voice (Samantha)
# -------------------------
def speak(text, pause=0.0):
    print(f"Assistant: {text}")

    # optional pause before speaking
    if pause > 0:
        time.sleep(pause)

    # Use macOS "say" command with Samantha
    os.system(f'say -v Samantha "{text}"')

