from recorder import record_audio
from asr import transcribe_audio
from intent_engine import parse_intent, execute_intent
from wakeword import detect_wake_word
from tts import speak, play_wake_sound, play_end_sound


def assistant_loop():
    # -----------------------------
    # Startup sound + announcement
    # -----------------------------
    try:
        play_wake_sound()
    except:
        print("[Warning] Startup sound failed.")

    speak("Assistant activated. Say Zara to wake me.", pause=0.2)
    print("Assistant: Ready and listening for wake word...\n")

    while True:

        # -----------------------------
        # 1. LISTEN FOR WAKE WORD
        # -----------------------------
        record_audio("samples/wake.wav", duration=3)
        wake_text = transcribe_audio("samples/wake.wav")

        print(f"Wake Text: {wake_text}")

        if not detect_wake_word(wake_text):
            continue

        # Wake beep
        try:
            play_wake_sound()
        except:
            print("[Warning] Wake beep error.")

        speak("Yes, I am listening.", pause=0.1)
        print("Assistant: Wake word detected. Listening for command...\n")

        # -----------------------------
        # 2. LISTEN FOR COMMAND
        # -----------------------------
        record_audio("samples/command.wav", duration=5)
        command_text = transcribe_audio("samples/command.wav")

        print(f"Command Text: {command_text}")

        # -----------------------------
        # 3. PARSE INTENT
        # -----------------------------
        intent, payload = parse_intent(command_text)
        print(f"Intent: {intent}, Payload: {payload}")

        # -----------------------------
        # 4. EXECUTE INTENT
        # -----------------------------
        result = execute_intent(intent, payload)

        # =============================
        # EXIT INTENT (STOP)
        # =============================
        if intent == "exit":
            speak("Goodbye. Turning off.", pause=0.1)
            print("Assistant shutting down.\n")

            try:
                play_end_sound()
            except:
                print("[Warning] End beep error.")

            break

        # =============================
        # NORMAL RESPONSE
        # =============================
        speak(result, pause=0.1)
        print(f"Assistant: {result}")

        try:
            play_end_sound()
        except:
            print("[Warning] End beep error.")

        print()  # formatting blank line

