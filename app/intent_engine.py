def parse_intent(text):
    if not text:
        return ("unknown", None, 0.0)

    text = text.lower().strip()

    # EXIT — Check FIRST (always strongest)
    if "bye" in text or "goodbye" in text or "stop" in text or "exit" in text:
        return ("exit", None, 0.99)

    # NAME SPELLING CORRECTION (must come BEFORE name learning)
    if "spelled" in text:
        after = text.split("spelled", 1)[-1].strip()

        after = (
            after.replace("-", " ")
                 .replace(",", " ")
                 .replace(".", "")
        )

        letters = after.split()

        if letters and all(len(ch) == 1 and ch.isalpha() for ch in letters):
            name = "".join(letters).title()
            return ("correct_name", name, 0.99)

    # REMEMBER NAME (persistent memory)
    if "name is" in text:
        name = text.split("name is")[-1].strip()
        if name:
            return ("remember_name", name, 0.95)

    # OPEN commands
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

    # TIME
    if "time" in text:
        return ("time", None, 0.90)

    # DATE
    if "date" in text:
        return ("date", None, 0.90)

    return ("unknown", None, 0.30)
   


import webbrowser
from datetime import datetime

def execute_intent(intent, payload):
        
    # EXIT returns a simple flag; assistant.py will handle speaking
    if intent == "exit":
        return "exit"
        
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
        
        return "Open what?"

   
    if intent == "youtube_search":
        webbrowser.get("open -a Safari %s").open(
            f"https://www.youtube.com/results?search_query={payload}"
        )
        return f"Searching YouTube for {payload}..."
    
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
    
    return "Sorry, I didn't understand that."

























