import difflib
import re

# Accepted wake-word variations
WAKE_WORDS = [
    "zara",
    "sara",
    "zahra",
    "zora",
    "zaraa"
]

SIMILARITY_THRESHOLD = 0.75


def normalize(text):
    """
    Lowercase, remove punctuation, extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()


def detect_wake_word(text):
    if not text:
        return False

    text = normalize(text)
    words = text.split()

    for word in words:
        matches = difflib.get_close_matches(
            word,
            WAKE_WORDS,
            n=1,
            cutoff=SIMILARITY_THRESHOLD
        )
        if matches:
            return True

    return False

