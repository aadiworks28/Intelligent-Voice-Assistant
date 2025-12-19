from recorder import record_audio
from asr import transcribe_audio
from intent_engine import parse_intent, execute_intent
from wakeword import detect_wake_word
from tts import speak, play_wake_sound, play_end_sound
from ui import user_says, assistant_says, system_msg
from mic_meter import show_mic_level



def assistant_loop():
    # -----------------------------
    # Startup
    # -----------------------------
    try:
        play_wake_sound()
    except:
        system_msg("Startup sound failed.")

    speak("Assistant activated. Say Zara to wake me.", pause=0.2)
    system_msg("Assistant ready. Listening for wake word.")

    active_session = False

    while True:

        # ==================================================
        # IDLE MODE → WAIT FOR WAKE WORD
        # ==================================================
        if not active_session:
            system_msg("Listening for wake word...")
            show_mic_level(duration=3)
            record_audio("samples/wake.wav", duration=3)
            wake_text = transcribe_audio("samples/wake.wav")

            if not detect_wake_word(wake_text):
                continue

            # Wake word detected
            system_msg("Wake word detected.")
            try:
                play_wake_sound()
            except:
                system_msg("Wake beep error.")

            speak("Yes, I am listening.", pause=0.1)
            assistant_says("Entering active session.")
            active_session = True
            continue

        # ==================================================
        # ACTIVE SESSION MODE → COMMANDS
        # ==================================================
        system_msg("Listening for command...")
        show_mic_level(duration=5)
        record_audio("samples/command.wav", duration=5)
        command_text = transcribe_audio("samples/command.wav")
        user_says(command_text)

        # Guard against silence / noise
        if not command_text or len(command_text.split()) < 2:
            speak("I didn't catch that. Please repeat.")
            continue

        # -----------------------------
        # Parse intent
        # -----------------------------
        intent, payload = parse_intent(command_text)

        # -----------------------------
        # Exit intent
        # -----------------------------
        if intent == "exit":
            speak("Goodbye. Turning off.", pause=0.1)
            assistant_says("Goodbye. Turning off.")
            system_msg("Assistant stopped.")

            try:
                play_end_sound()
            except:
                system_msg("End beep error.")

            active_session = False
            system_msg("Back to wake-word mode.")
            continue

        # -----------------------------
        # Execute intent
        # -----------------------------
        result = execute_intent(intent, payload)

        if result:
            speak(result, pause=0.1)
            assistant_says(result)

        try:
            play_end_sound()
        except:
            system_msg("End beep error.")

