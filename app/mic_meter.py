import sounddevice as sd
import numpy as np
import sys
import time

def show_mic_level(duration=3):
    """
    Displays a live microphone volume meter for `duration` seconds.
    """
    samplerate = 16000
    block_duration = 0.1  # seconds
    block_size = int(samplerate * block_duration)

    def callback(indata, frames, time_info, status):
        volume_norm = np.linalg.norm(indata) * 10
        bars = int(min(volume_norm, 20))
        meter = "█" * bars + "░" * (20 - bars)

        sys.stdout.write(f"\r🎤 Listening  {meter}")
        sys.stdout.flush()

    with sd.InputStream(
        channels=1,
        samplerate=samplerate,
        blocksize=block_size,
        callback=callback,
    ):
        time.sleep(duration)

    sys.stdout.write("\n")

