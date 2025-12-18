def detect_wake_word(text):
    """
    Returns True if wake word 'zara' is detected in the text.
    """
    if not text:
        return False

    text = text.lower().strip()

    wake_words = [
        "zara",
        "hey zara",
        "hi zara",
        "okay zara",
        "hello zara"
    ]

    return any(w in text for w in wake_words)

