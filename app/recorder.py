import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="samples/output.wav", duration=5, fs=44100):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()   # wait for recording to finish
    sd.stop()   # <<< IMPORTANT FIX
    write(filename, fs, recording)
    print(f"Saved recording to {filename}")

