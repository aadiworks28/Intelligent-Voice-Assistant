from recorder import record_audio
from asr import transcribe_audio
from intent_engine import parse_intent, execute_intent
from wakeword import detect_wake_word
from tts import speak, play_wake_sound, play_end_sound


def assistant_loop():
    # Startup message
    try:
        play_wake_sound()
    except:
        pass

    speak("Assistant activated. Say Zara to wake me.", pause=0.2)
    print("Assistant: Ready and listening for wake word...")

    while True:
        # 1. Listen for wake word
        record_audio(filename="samples/wake.wav", duration=3)
        wake_text = transcribe_audio("samples/wake.wav")

        print(f"Wake Text: {wake_text}")

        if detect_wake_word(wake_text):

            # Wake sound (if available)
            try:
                play_wake_sound()
            except:
                pass

            speak("Yes, I am listening.", pause=0.1)
            print("Assistant: Wake word detected. Listening for command...")

            # 2. Listen for command
            record_audio(filename="samples/command.wav", duration=5)
            command_text = transcribe_audio("samples/command.wav")

            print(f"Command Text: {command_text}")

            # 3. Parse intent
            intent, payload = parse_intent(command_text)
            print(f"Intent: {intent}, Payload: {payload}")

            # 4. Execute intent
            result = execute_intent(intent, payload)

            # If exit intent → don't speak twice
            if intent == "exit":
                speak("Goodbye. Turning off.", pause=0.1)
                print("Assistant shutting down.")
                
                try:
                    play_end_sound()
                except:
                    pass

                break

            # 5. Speak and print result normally
            speak(result, pause=0.1)
            print("Assistant:", result)

            # Ending tone
            try:
                play_end_sound()
            except:
                pass

