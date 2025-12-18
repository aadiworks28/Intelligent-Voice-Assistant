import whisper

print("Loading Whisper model once...")
model = whisper.load_model("base")

def transcribe_audio(filepath):
    print("Transcribing...")
    result = model.transcribe(filepath)
    text = result["text"].strip()
    print("Text:", text)
    return text

