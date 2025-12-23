from recorder import record_audio
from asr import transcribe_audio
from intent_engine import parse_intent, execute_intent
from wakeword import detect_wake_word
from tts import speak, play_wake_sound, play_end_sound
from ui import user_says, assistant_says, system_msg
from memory import load_memory, save_memory
from tasks import add_task, deactivate_all
from scheduler import scheduler_loop

import threading
import time


def reset_session_state():
    return None, None, None, None


mic_lock = threading.Lock()


def listen_with_meter(filename, duration):
    record_audio(filename=filename, duration=duration)


def assistant_loop():
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

    threading.Thread(target=scheduler_loop, daemon=True).start()

    last_platform, last_intent, last_payload, last_command_time = reset_session_state()
    active_session = False
    SESSION_TIMEOUT = 20

    while True:

        if not active_session:
            system_msg("Listening for wake word...")
            listen_with_meter("samples/wake.wav", 3)

            wake_text = transcribe_audio("samples/wake.wav").lower().strip()
            if not detect_wake_word(wake_text):
                continue

            last_command_time = time.time()
            play_wake_sound()
            speak("Yes, I am listening.", pause=0.1)
            assistant_says("Entering active session.")

            active_session = True
            last_platform, last_intent, last_payload = None, None, None
            continue

        if time.time() - last_command_time > SESSION_TIMEOUT:
            speak("Going idle.")
            assistant_says("Session timed out.")
            active_session = False
            last_platform, last_intent, last_payload, last_command_time = reset_session_state()
            continue

        system_msg("Listening for command...")
        listen_with_meter("samples/command.wav", 7)

        command_text = (
            transcribe_audio("samples/command.wav")
            .lower()
            .replace(".", "")
            .replace(",", "")
            .strip()
        )

        user_says(command_text)

        intent, payload, confidence = parse_intent(command_text)
        words = command_text.split()

        NOISE_WORDS = {
            "uh", "um", "hmm", "huh", "ah",
            "okay", "ok", "yes", "yeah",
            "no", "please", "hey", "hi",
        }

        if intent == "exit":
            speak("Goodbye. Turning off.", pause=0.1)
            assistant_says("Goodbye. Turning off.")
            play_end_sound()
            active_session = False
            last_platform, last_intent, last_payload, last_command_time = reset_session_state()
            continue

        if intent == "correct_name":
            memory["user_name"] = payload
            save_memory(memory)
            last_command_time = time.time()
            speak(f"Thanks for correcting me. I'll remember your name as {payload}.")
            assistant_says(f"Corrected name to: {payload}")
            continue

        if intent == "remember_name":
            memory["user_name"] = payload.title()
            save_memory(memory)
            last_command_time = time.time()
            speak(f"Got it. I'll remember your name, {payload.title()}.")
            assistant_says(f"Saved name: {payload.title()}")
            continue

        if intent == "set_alarm":
            add_task("alarm", payload, "Wake up")
            last_command_time = time.time()
            speak("Alarm set.")
            continue

        if intent == "set_reminder":
            trigger_time, message = payload
            add_task("reminder", trigger_time, message)
            last_command_time = time.time()
            speak("Reminder set.")
            continue

        if intent == "cancel_alarm":
            deactivate_all("alarm")
            last_command_time = time.time()
            speak("All alarms cancelled.")
            continue

        if intent == "cancel_reminder":
            deactivate_all("reminder")
            last_command_time = time.time()
            speak("All reminders cancelled.")
            continue

        if not words or all(w in NOISE_WORDS for w in words):
            speak("I didn't catch a command. Please try again.")
            assistant_says("Ignored noise / filler input.")
            continue

        if intent not in ["remember_name", "correct_name"] and confidence < 0.6:
            speak("I'm not sure I understood that. Could you rephrase?")
            assistant_says("Low confidence intent.")
            continue

        if intent == "open" and payload is None:
            speak("Which app should I open?")
            assistant_says("Open intent without target.")
            continue

        if intent == "search" and not payload:
            speak("What should I search for?")
            assistant_says("Search intent without query.")
            continue

        if intent == "search" and last_platform == "youtube":
            result = execute_intent("youtube_search", payload)
            last_command_time = time.time()
            speak(result)
            assistant_says(result)
            continue

        result = "I didn't understand that yet." if intent == "unknown" else execute_intent(intent, payload)

        if result:
            last_command_time = time.time()
            speak(result)
            assistant_says(result)

            if intent == "open" and payload in ["youtube", "google"]:
                last_platform = payload

        play_end_sound()

