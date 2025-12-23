import re
from datetime import datetime, timedelta
import webbrowser


NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}


def normalize_numbers(text):
    for word, num in NUMBER_WORDS.items():
        text = text.replace(f"in {word} minute", f"in {num} minute")
        text = text.replace(f"in {word} minutes", f"in {num} minutes")
    return text


def parse_time_at(text):
    match = re.search(r"at (\d{1,2})(?:\s)?(am|pm)?", text)
    if not match:
        return None

    hour = int(match.group(1))
    meridian = match.group(2)

    if meridian == "pm" and hour < 12:
        hour += 12
    if meridian == "am" and hour == 12:
        hour = 0

    now = datetime.now()
    return now.replace(hour=hour, minute=0).strftime("%Y-%m-%d %H:%M")


def parse_time_in(text):
    match = re.search(r"in (\d+) minutes?", text)
    if not match:
        return None

    minutes = int(match.group(1))
    return (datetime.now() + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M")


def parse_intent(text):
    if not text:
        return ("unknown", None, 0.0)

    text = normalize_numbers(text.lower().strip())

    # EXIT — strongest intent
    if "bye" in text or "goodbye" in text or "stop" in text or "exit" in text:
        return ("exit", None, 0.99)

    # NAME SPELLING CORRECTION
    if "spelled" in text:
        after = text.split("spelled", 1)[-1].strip()
        after = after.replace("-", " ").replace(",", " ").replace(".", "")
        letters = after.split()

        if letters and all(len(ch) == 1 and ch.isalpha() for ch in letters):
            name = "".join(letters).title()
            return ("correct_name", name, 0.99)

    # REMEMBER NAME
    if "name is" in text:
        name = text.split("name is")[-1].strip()
        if name:
            return ("remember_name", name, 0.95)

    # SET ALARM
    if "set alarm" in text:
        text = normalize_numbers(text)
        trigger = parse_time_in(text) or parse_time_at(text)
        if trigger:
            return ("set_alarm", trigger, 0.95)

    # SET REMINDER
    if "remind me" in text:
        text = normalize_numbers(text)
        trigger = parse_time_in(text) or parse_time_at(text)
        if trigger:
            message = text.replace("remind me", "").strip()
            return ("set_reminder", (trigger, message), 0.95)


    # CANCEL TASKS
    if "cancel alarm" in text:
        return ("cancel_alarm", None, 0.95)

    if "cancel reminder" in text:
        return ("cancel_reminder", None, 0.95)

    # OPEN COMMANDS
    if "open" in text:
        if "youtube" in text:
            return ("open", "youtube", 0.95)
        if "google" in text:
            return ("open", "google", 0.95)
        if "instagram" in text:
            return ("open", "instagram", 0.95)
        return ("open", None, 0.60)

    # SEARCH
    if "search" in text:
        query = text.replace("search", "").strip()
        if query:
            return ("search", query, 0.85)
        return ("search", None, 0.60)

    # TIME / DATE
    if "time" in text:
        return ("time", None, 0.90)

    if "date" in text:
        return ("date", None, 0.90)

    return ("unknown", None, 0.30)


def execute_intent(intent, payload):
    if intent == "open":
        if payload == "youtube":
            webbrowser.get("open -a Safari %s").open("https://youtube.com")
            return "Opening YouTube..."

        if payload == "google":
            webbrowser.get("open -a Safari %s").open("https://google.com")
            return "Opening Google..."

        if payload == "instagram":
            webbrowser.get("open -a Safari %s").open("https://instagram.com")
            return "Opening Instagram..."

    if intent == "search":
        webbrowser.get("open -a Safari %s").open(
            f"https://google.com/search?q={payload}"
        )
        return f"Searching for {payload}..."

    if intent == "time":
        now = datetime.now().strftime("%H:%M")
        return f"The time is {now}."

    if intent == "date":
        today = datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {today}."

    return None























