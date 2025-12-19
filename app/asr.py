import whisper

print("Loading Whisper model once...")
model = whisper.load_model("base")

def transcribe_audio(filepath):
    print("Transcribing...")
    result = model.transcribe(
        filepath,
        fp16=False   # 🔧 FIX: disable FP16 on CPU
    )
    text = result["text"].strip()
    print("Text:", text)
    return text

