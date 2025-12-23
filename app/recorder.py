import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import sys
import time


def record_audio(filename="samples/output.wav", duration=5, fs=44100):
    print(f"Recording for {duration} seconds...")

    frames = []
    start_time = time.time()

    def callback(indata, frames_count, time_info, status):
        volume = np.linalg.norm(indata) * 10
        bars = int(min(volume, 20))
        meter = "█" * bars + "░" * (20 - bars)
        sys.stdout.write(f"\r🎤 Listening {meter}")
        sys.stdout.flush()

        frames.append(indata.copy())

    with sd.InputStream(
        samplerate=fs,
        channels=1,
        callback=callback
    ):
        sd.sleep(int(duration * 1000))

    audio = np.concatenate(frames, axis=0)
    write(filename, fs, audio)

    sys.stdout.write("\n")
    print(f"Saved recording to {filename}")

