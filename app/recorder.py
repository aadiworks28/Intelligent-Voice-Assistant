import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="samples/output.wav", duration=5, fs=44100):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording finishes
    write(filename, fs, audio)
    print(f"Saved recording to {filename}")

if __name__ == "__main__":
    record_audio()
