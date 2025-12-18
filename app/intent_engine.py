def parse_intent(text):
    if not text:
        return ("unknown", None)
        
    text = text.lower().strip()

    # EXIT
    if any(word in text for word in ["bye", "goodbye", "stop", "exit", "shut down"]):
        return ("exit", None)

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

    # UNKNOWN
    return ("unknown", None)



import webbrowser
from datetime import datetime

def execute_intent(intent, payload):
    if intent == "open":
        ...
    if intent == "search":
        ...
    if intent == "time":
        ...
    if intent == "date":
        ...

    # EXIT should NOT return a goodbye message
    if intent == "exit":
        return "exit"

    return "Sorry, I didn't understand that."






























