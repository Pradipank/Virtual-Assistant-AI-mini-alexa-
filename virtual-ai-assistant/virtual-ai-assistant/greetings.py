"""Greeting logic and name capture (FR-01, FR-02).

The assistant stores the user's name in the session and reuses it in later
responses. Remembering a value from earlier in the conversation is the simplest
form of "memory" in an AI system.
"""

ASSISTANT_NAME = "Mini Alexa"
DEFAULT_NAME = "friend"        # used if the user never gives a usable name
MAX_NAME_ATTEMPTS = 3          # how many times we ask before using DEFAULT_NAME
MAX_NAME_LENGTH = 30           # keeps absurdly long input from becoming a "name"
NAME_PREFIXES = ("my name is ", "i am ", "i'm ", "call me ")


def clean_name(raw_text):
    """Tidy raw input into a display name ("  my name is priya " -> "Priya")."""
    cleaned = " ".join(raw_text.split())            # collapse extra spaces
    lowered = cleaned.lower()
    for prefix in NAME_PREFIXES:                    # keyword detection on the input
        if lowered.startswith(prefix):
            cleaned = cleaned[len(prefix):]
            break
    return cleaned.title()


def is_valid_name(candidate):
    """A valid name has at least one letter and is not unreasonably long."""
    has_letter = any(char.isalpha() for char in candidate)
    return has_letter and len(candidate) <= MAX_NAME_LENGTH


def get_user_name(input_fn=input, print_fn=print):
    """Ask for the user's name (FR-01) and return it. Falls back to DEFAULT_NAME."""
    print_fn(f"Assistant: Hi! I'm {ASSISTANT_NAME}. What's your name?")
    for _ in range(MAX_NAME_ATTEMPTS):
        candidate = clean_name(input_fn("You: "))
        if is_valid_name(candidate):
            return candidate
        print_fn("Assistant: I didn't catch that. Could you type just your name?")
    return DEFAULT_NAME


def build_greeting(name):
    """Welcome message shown right after the name is stored (user flow step 4)."""
    return f"Nice to meet you, {name}! Type 'help' to see what I can do."


def respond_hello(name):
    """Reply to 'hi', 'hello', 'good morning', etc. and reuse the name (FR-02)."""
    return f"Hello, {name}! How can I help you today?"


def respond_how_are_you(name):
    """Small-talk reply."""
    return f"I'm running perfectly, {name}. Thanks for asking! How about you?"


def respond_thanks(name):
    """Reply to 'thanks'."""
    return f"You're welcome, {name}!"


def respond_about():
    """Reply to 'who are you'."""
    return (f"I'm {ASSISTANT_NAME}, a rule-based virtual assistant written in plain Python. "
            "Type 'concepts' to see how I demonstrate AI, ML and DL ideas.")


def respond_name(name):
    """Reply to 'what is my name'."""
    return f"Your name is {name}."
