def parse_intent(text):
    if not text:
        return ("unknown", None)

    text = text.lower().strip()

    # OPEN APPS / SERVICES
    if "open" in text:
        if "youtube" in text:
            return ("open", "youtube")
        if "google" in text:
            return ("open", "google")
        if "instagram" in text:
            return ("open", "instagram")
        return ("open", None)

    # SEARCH
    if "search" in text:
        query = text.replace("search", "").strip()
        return ("search", query)

    # TIME
    if "time" in text:
        return ("time", None)

    # DATE
    if "date" in text:
        return ("date", None)

    return ("unknown", None)


import webbrowser
from datetime import datetime

def execute_intent(intent, payload):
    if intent == "open":
        if payload == "youtube":
            webbrowser.open("https://youtube.com")
            return "Opening YouTube..."
        if payload == "google":
            webbrowser.open("https://google.com")
            return "Opening Google..."
        if payload == "instagram":
            webbrowser.open("https://instagram.com")
            return "Opening Instagram..."
        return "Open what?"

    if intent == "search":
        webbrowser.open(f"https://www.google.com/search?q={payload}")
        return f"Searching for {payload}..."

    if intent == "time":
        now = datetime.now().strftime("%H:%M")
        return f"The time is {now}."

    if intent == "date":
        today = datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {today}."

    return "Sorry, I didn't understand that."






























