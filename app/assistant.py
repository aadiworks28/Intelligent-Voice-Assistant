from recorder import record_audio
from asr import transcribe_audio
from intent_engine import parse_intent, execute_intent
from wakeword import detect_wake_word
from tts import speak, play_wake_sound, play_end_sound
from ui import user_says, assistant_says, system_msg
from mic_meter import show_mic_level
from memory import load_memory, save_memory
import threading
import time

def reset_session_state():
    return None, None, None, None


mic_lock = threading.Lock()


def listen_with_meter(filename, duration):
    if mic_lock.locked():
        return  # Prevent overlapping meters

    with mic_lock:
        meter_thread = threading.Thread(
            target=show_mic_level,
            kwargs={"duration": duration},
            daemon=True
        )

        record_thread = threading.Thread(
            target=record_audio,
            kwargs={"filename": filename, "duration": duration},
            daemon=True
        )

        meter_thread.start()
        record_thread.start()

        record_thread.join()
        meter_thread.join()


def assistant_loop():
    # -----------------------------
    # Startup
    # -----------------------------
   
    try:
        play_wake_sound()
    except:
        system_msg("Startup sound failed.")

    memory = load_memory()

    name = memory.get("user_name")
    if name:
        speak(f"Assistant activated. Hello {name}. Say Zara to wake me.", pause=0.2)
    else:
        speak("Assistant activated. Say Zara to wake me.", pause=0.2)

    system_msg("Assistant ready. Listening for wake word.")

 
    last_platform, last_intent, last_payload, last_command_time = reset_session_state()

    active_session = False
    command_history = []

    SESSION_TIMEOUT = 20  # seconds
 
    while True:

        # ==================================================
        # IDLE MODE → WAIT FOR WAKE WORD
        # ==================================================
        if not active_session:
            system_msg("Listening for wake word...")
            listen_with_meter("samples/wake.wav", duration=3)

            wake_text = transcribe_audio("samples/wake.wav")
            wake_text = wake_text.strip().lower()


            if not detect_wake_word(wake_text):
                continue

            system_msg("Wake word detected.")
            try:
                play_wake_sound()
            except:
                system_msg("Wake beep error.")

            speak("Yes, I am listening.", pause=0.1)
            assistant_says("Entering active session.")

            active_session = True
            last_command_time = time.time()
            last_platform = None
            last_intent = None
            last_payload = None


            continue

        # -----------------------------
        # Session timeout check
        # -----------------------------
        if last_command_time and (time.time() - last_command_time) > SESSION_TIMEOUT:
            speak("Going idle.")
            assistant_says("Session timed out.")
            system_msg("Returned to wake-word mode.")

            active_session = False
            last_platform, last_intent, last_payload, last_command_time = reset_session_state()

            continue

        # ==================================================
        # ACTIVE SESSION MODE → COMMANDS
        # ==================================================
        system_msg("Listening for command...")
        listen_with_meter("samples/command.wav", duration=7)

        command_text = transcribe_audio("samples/command.wav")
        command_text = (
            command_text
            .lower()
            .replace(".", "")
            .replace(",", "")
            .strip()
        ) 
        user_says(command_text)
        command_history.append(command_text)

        # -----------------------------
        # Parse intent FIRST (FIX)
        # -----------------------------
        intent, payload, confidence = parse_intent(command_text)

        # -----------------------------
        # Correct stored name  
        # -----------------------------
        if intent == "correct_name":
            memory["user_name"] = payload
            save_memory(memory)
            
            speak(f"Thanks for correcting me. I'll remember your name as {payload}.")
            assistant_says(f"Corrected name to: {payload}")
            
            last_command_time = time.time()
            continue


        # -----------------------------
        # Noise & filler filtering
        # -----------------------------
        NOISE_WORDS = {
            "uh", "um", "hmm", "huh", "ah", "okay", "ok",
            "yes", "yeah", "no", "please", "hey", "hi",
        }
        words = command_text.lower().split()

        if intent != "exit":
            if len(words) <= 1 or all(w in NOISE_WORDS for w in words):
                speak("I didn't catch a command. Please try again.")
                assistant_says("Ignored noise / filler input.")
                continue

        if not command_text or len(command_text.split()) < 2:
            speak("I didn't catch that. Please repeat.")
            continue

        # -----------------------------
        # Open intent without payload
        # -----------------------------
        if intent == "open" and payload is None:
            speak("Which app should I open?")
            assistant_says("Open intent without target.")
            continue

        # -----------------------------
        # Context-based search routing
        # -----------------------------
        if intent == "search" and last_platform == "youtube":
            result = execute_intent("youtube_search", payload)
            speak(result, pause=0.1)
            assistant_says(result)
            last_command_time = time.time()
            continue

        # -----------------------------
        # Confidence check
        # -----------------------------
        if intent not in ["remember_name"] and confidence < 0.6 and len(words) > 1:
            speak("I'm not sure I understood that. Could you rephrase?")
            assistant_says("Low confidence intent.")
            continue

        # -----------------------------
        # Empty payload protection
        # -----------------------------
        if intent == "search" and not payload:
            speak("What should I search for?")
            assistant_says("Search intent without query.")
            continue

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
            last_platform, last_intent, last_payload, last_command_time = reset_session_state()

            continue

        # -----------------------------
        # Remember user's name (PERSISTENT MEMORY)
        # -----------------------------
        if intent == "remember_name":
            memory["user_name"] = payload.title()
            save_memory(memory)

            speak(f"Got it. I'll remember your name, {payload.title()}.")
            assistant_says(f"Saved name: {payload.title()}")

            last_command_time = time.time()
            continue


        # -----------------------------
        # Execute intent
        # -----------------------------
        if intent == "unknown":
            result = "I didn't understand that yet."
        else:
            result = execute_intent(intent, payload) 

        if result:
            name = memory.get("user_name")
            if name and "I" in result:
                result = result.replace("I", f"I, {name},")
            speak(result, pause=0.1)
            assistant_says(result)
            last_command_time = time.time()

            if intent == "open" and payload in ["youtube", "google"]:
                last_platform = payload

        try:
            play_end_sound()
        except:
            system_msg("End beep error.")

