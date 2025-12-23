from tts import speak, play_alarm_sound, play_reminder_sound
from memory import load_memory
import time
from datetime import datetime
from tasks import load_tasks, save_tasks
from tts import speak, play_end_sound


def scheduler_loop():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        tasks = load_tasks()
        updated = False

        for task in tasks:
            if task["active"] and task["trigger_time"] == now:
                if task["type"] == "alarm":
                    speak("Alarm ringing.")
                    play_end_sound()
                    speak(task["message"])
                else:
                    memory = load_memory()
                    name = memory.get("user_name", "")

                    if task["type"] == "alarm":
                        play_alarm_sound()
                        speak(f"{name}, your alarm is ringing.")

                    elif task["type"] == "reminder":
                        play_reminder_sound()
                        speak(f"{name}, this is your reminder. {task['message']}")

                task["active"] = False
                updated = True

        if updated:
            save_tasks(tasks)

        time.sleep(30)

