from recorder import record_audio
from asr import transcribe_audio
from intent_engine import parse_intent, execute_intent

def run_assistant():
    print("Speak after the beep...")
    record_audio()   # RECORDS audio

    print("Analyzing speech...")
    text = transcribe_audio()   # IMPORTANT: CAPTURE RETURN VALUE

    print("You said:", text)

    intent, payload = parse_intent(text)
    result = execute_intent(intent, payload)

    print("Assistant:", result)

if __name__ == "__main__":
    run_assistant()

