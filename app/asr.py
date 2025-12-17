import whisper

def transcribe_audio(filepath="samples/output.wav"):
    print("Loading model...")
    model = whisper.load_model("base")

    print("Transcribing...")
    result = model.transcribe(filepath)
    print("Text:", result["text"])

if __name__ == "__main__":
    transcribe_audio()
