"""Mini Alexa - Virtual AI Assistant: program entry point and main loop.

Run with:  python main.py

Every loop iteration follows the request-classification-response cycle from
the PRD:  input -> normalize -> keyword/pattern match -> respond -> print.
"""

import re
from collections import Counter

import ai_concepts
import calculator
import content
import datetime_utils
import game
import greetings
import help_menu

BANNER_WIDTH = 43
PHRASE_WEIGHT = 2      # a matched phrase ("what time") counts more than one word
MATH_BONUS = 3         # a valid "number operator number" pattern is strong evidence
FALLBACK_MESSAGE = "I'm not sure I understood that \u2014 type 'help' to see what I can do."
NAME_PATTERN = re.compile(r"my name is ([a-z][a-z' -]*)")

# Keyword rules: (intent, single trigger words, trigger phrases).
# Detection is a tiny "similarity match": each intent is scored by how many of
# its keywords appear in the text and the best score wins. Order breaks ties.
INTENT_RULES = [
    ("exit", {"exit", "quit", "bye", "goodbye"}, []),
    ("help", {"help", "commands", "menu"}, ["what can you do"]),
    ("calculate", {"calculate", "calc", "compute", "plus", "minus", "times"},
     ["divided by", "multiplied by"]),
    ("recommend", {"recommend", "suggest", "suggestion", "activity", "bored"},
     ["what should i do"]),
    ("time", {"time", "clock"}, ["what time"]),
    ("date", {"date", "today", "day"}, ["what day"]),
    ("quote", {"quote", "quotes", "motivate", "motivation", "motivational", "inspire"}, []),
    ("joke", {"joke", "jokes", "funny", "laugh"}, []),
    ("fact", {"fact", "facts", "trivia"}, []),
    ("game", {"game", "play", "guess", "guessing"}, []),
    ("perceptron", {"perceptron", "neuron", "neural"}, []),
    ("concepts", {"concepts", "ai", "ml", "dl"},
     ["machine learning", "deep learning", "artificial intelligence"]),
    ("stats", {"stats", "favourite", "favorite", "preferences"}, ["what do i like"]),
    ("name", set(), ["my name", "who am i"]),
    ("about", set(), ["who are you", "your name", "about yourself"]),
    ("how_are_you", set(), ["how are you"]),
    ("thanks", {"thanks", "thank", "thx"}, []),
    ("greeting", {"hi", "hello", "hey", "hola", "howdy", "namaste"},
     ["good morning", "good afternoon", "good evening"]),
]


def normalize(raw_text):
    """Lowercase the text and collapse extra spaces so matching is consistent."""
    return " ".join(raw_text.lower().split())


def detect_intent(text):
    """Return the best-matching intent name for ``text``, or None if nothing matches."""
    tokens = set(re.findall(r"[a-z0-9']+", text))
    best_intent = None
    best_score = 0
    for intent, words, phrases in INTENT_RULES:
        score = len(tokens & words)
        score += PHRASE_WEIGHT * sum(1 for phrase in phrases if phrase in text)
        if intent == "calculate" and calculator.looks_like_math(text):
            score += MATH_BONUS
        if score > best_score:
            best_intent, best_score = intent, score
    return best_intent


def respond_greeting(session):
    """Reply to a greeting using the stored name."""
    return greetings.respond_hello(session["name"])


def respond_time():
    """Report the current time."""
    return datetime_utils.get_current_time()


def respond_date():
    """Report the current date."""
    return datetime_utils.get_current_date()


def respond_calculator(text):
    """Run the calculator on the user's text."""
    return calculator.run_calculation(text)


def respond_quote():
    """Return a random motivational quote."""
    return content.get_random_quote()


def respond_joke():
    """Return a random joke."""
    return content.get_random_joke()


def respond_fact():
    """Return a random fact."""
    return content.get_random_fact()


def respond_game(session, input_fn, print_fn):
    """Play the number guessing game."""
    return game.play_guessing_game(session["name"], input_fn, print_fn)


def respond_help():
    """Return the help menu text."""
    return help_menu.format_help()


def respond_recommendation(session, text):
    """Recommend an activity for the current hour, or for an hour typed by the user."""
    hour = ai_concepts.extract_hour(text)
    if hour is None:
        hour = datetime_utils.get_current_hour()
    return ai_concepts.respond_recommendation(session["name"], hour)


def respond_name(session, text):
    """Handle 'my name is X' (rename) and 'what is my name'."""
    match = NAME_PATTERN.search(text)
    if match is None:
        return greetings.respond_name(session["name"])
    new_name = greetings.clean_name(match.group(1))
    if not greetings.is_valid_name(new_name):
        return "That doesn't look like a name I can use. Try: my name is Priya"
    session["name"] = new_name
    return f"Okay, I'll call you {new_name} from now on."


def end_session(session):
    """Stop the main loop and return the goodbye message (FR-11)."""
    session["running"] = False
    return f"Goodbye, {session['name']}! Have a great day."


def route(intent, text, session, input_fn, print_fn):
    """Send the detected intent to its response function and return the reply text."""
    if intent == "greeting":
        reply = respond_greeting(session)
    elif intent == "time":
        reply = respond_time()
    elif intent == "date":
        reply = respond_date()
    elif intent == "calculate":
        reply = respond_calculator(text)
    elif intent == "quote":
        reply = respond_quote()
    elif intent == "joke":
        reply = respond_joke()
    elif intent == "fact":
        reply = respond_fact()
    elif intent == "game":
        reply = respond_game(session, input_fn, print_fn)
    elif intent == "help":
        reply = respond_help()
    elif intent == "recommend":
        reply = respond_recommendation(session, text)
    elif intent == "perceptron":
        reply = ai_concepts.perceptron_demo(session["name"], input_fn, print_fn)
    elif intent == "concepts":
        reply = ai_concepts.explain_concepts()
    elif intent == "stats":
        reply = ai_concepts.summarize_preferences(session["name"], session["usage"])
    elif intent == "name":
        reply = respond_name(session, text)
    elif intent == "about":
        reply = greetings.respond_about()
    elif intent == "how_are_you":
        reply = greetings.respond_how_are_you(session["name"])
    elif intent == "thanks":
        reply = greetings.respond_thanks(session["name"])
    elif intent == "exit":
        reply = end_session(session)
    else:
        reply = FALLBACK_MESSAGE
    return reply


def print_banner(print_fn=print):
    """Print the title banner from the PRD wireframe."""
    line = "=" * BANNER_WIDTH
    print_fn(line)
    print_fn("MINI ALEXA - VIRTUAL ASSISTANT".center(BANNER_WIDTH).rstrip())
    print_fn(line)


def run_assistant(input_fn=input, print_fn=print):
    """Main loop. ``input_fn``/``print_fn`` can be replaced for automated testing."""
    print_banner(print_fn)
    try:
        name = greetings.get_user_name(input_fn, print_fn)
        session = {"name": name, "usage": Counter(), "running": True}
        print_fn(f"Assistant: {greetings.build_greeting(name)}")

        while session["running"]:
            text = normalize(input_fn("You: "))
            if not text:
                print_fn("Assistant: Say something and I'll do my best to help.")
                continue
            intent = detect_intent(text)
            if intent is not None:
                session["usage"][intent] += 1        # session memory used by 'stats'
            reply = route(intent, text, session, input_fn, print_fn)
            print_fn(f"Assistant: {reply}")
    except (EOFError, KeyboardInterrupt):
        print_fn("\nAssistant: Session interrupted. Goodbye!")


if __name__ == "__main__":
    run_assistant()
