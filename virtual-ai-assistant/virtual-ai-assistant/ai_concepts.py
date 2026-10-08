"""AI / ML / DL concept demonstrations (FR-13, FR-14).

NOTHING in this file is trained. Every "model" below is plain Python arithmetic
and if/elif logic that illustrates an idea you will meet again with real
libraries in later projects.

    AI  -> rule-based decision making        (recommend_activity)
    ML  -> classification / "learning" from the session (recommend_activity,
           summarize_preferences)
    DL  -> the artificial neuron (perceptron) and a tiny layered network
"""

import math
import re

# ---------------------------------------------------------------------------
# Rule-based decision making  (AI concept + decision-tree / classification analogy)
# ---------------------------------------------------------------------------

LAST_HOUR = 23
NOON = 12


def recommend_activity(hour):
    """Return (category, advice) for an hour of the day using an if/elif chain.

    Concept: the hour is the input *feature*; each branch is a decision-tree
    split; the returned category is the *predicted label*. A trained classifier
    does the same job, except it learns its splits from data instead of a
    developer typing them. Raises ValueError if the hour is not 0-23.
    """
    if not 0 <= hour <= LAST_HOUR:
        raise ValueError("The hour must be between 0 and 23.")

    if hour < 5:
        category, advice = "rest", "It's the middle of the night. The best activity is sleep."
    elif hour < 8:
        category, advice = "exercise", "A great time for a stretch, a walk or a workout."
    elif hour < 10:
        category, advice = "breakfast", "Have a healthy breakfast and plan your day."
    elif hour < 12:
        category, advice = "focused work", "Your mind is fresh. Tackle your hardest task now."
    elif hour < 14:
        category, advice = "lunch", "Time for lunch and a short break away from the screen."
    elif hour < 17:
        category, advice = "learning", "Good time for a project, a course or some coding practice."
    elif hour < 19:
        category, advice = "outdoors", "Get some fresh air: a walk, a game or a catch-up with friends."
    elif hour < 21:
        category, advice = "dinner", "Enjoy dinner and spend time with family or friends."
    elif hour < LAST_HOUR:
        category, advice = "relaxing", "Wind down with a book, music or light reading."
    else:
        category, advice = "sleep", "Time to get ready for bed so you wake up refreshed."
    return category, advice


def format_hour(hour):
    """Show an hour in 12-hour style: 15 -> '3:00 PM'."""
    suffix = "AM" if hour < NOON else "PM"
    return f"{hour % NOON or NOON}:00 {suffix}"


def extract_hour(text):
    """Find an hour in the user's text ('recommend at 9', 'suggest 7 pm'). None if absent."""
    match = re.search(r"\b(\d{1,2})(?::\d{2})?\s*(am|pm)?\b", text)
    if match is None:
        return None
    hour = int(match.group(1))
    period = match.group(2)
    if period == "pm" and hour < NOON:
        hour += NOON
    elif period == "am" and hour == NOON:
        hour = 0
    return hour


def respond_recommendation(name, hour):
    """Build the full recommendation message, or an error message for a bad hour."""
    try:
        category, advice = recommend_activity(hour)
    except ValueError as error:
        return str(error)
    return (f"{name}, it's {format_hour(hour)}. My rules classify this time as "
            f"'{category}'. {advice}")


# ---------------------------------------------------------------------------
# Learning from the session  (ML analogy: remembering a user's preferences)
# ---------------------------------------------------------------------------

PREFERENCE_LABELS = {
    "joke": "jokes",
    "quote": "motivational quotes",
    "fact": "random facts",
    "game": "the guessing game",
    "calculate": "calculations",
    "recommend": "activity recommendations",
    "perceptron": "the perceptron demo",
}


def summarize_preferences(name, usage):
    """Tell the user what they seem to like, based on how often they used each feature.

    Concept: a recommender "learns" a preference from past behaviour. Here the
    learning is just counting, but the idea (past data -> prediction) is the same.
    """
    counts = {key: usage[key] for key in PREFERENCE_LABELS if usage.get(key)}
    if not counts:
        return (f"I haven't learned your preferences yet, {name}. "
                "Ask for a joke, quote or fact and I'll start keeping track!")
    favourite = max(counts, key=lambda feature: counts[feature])
    times = counts[favourite]
    return (f"So far you've asked for {PREFERENCE_LABELS[favourite]} {times} "
            f"{'time' if times == 1 else 'times'}, {name}, so I'd guess that's your favourite!")


# ---------------------------------------------------------------------------
# Deep learning building blocks: the perceptron  (artificial neuron)
# ---------------------------------------------------------------------------

# Scenario: "Should I go for a walk?"  Inputs: weather rating (0-10),
# free time in hours (0-5), energy level (0-10).
INPUT_NAMES = ("weather", "free time", "energy")
INPUT_PROMPTS = ("Weather rating from 0 to 10: ",
                 "Free time in hours (0 to 5): ",
                 "Energy level from 0 to 10: ")
PERCEPTRON_WEIGHTS = (0.6, 0.5, 0.4)   # fixed: how much each input matters
PERCEPTRON_BIAS = -5.0                 # fixed: how hard it is for the neuron to "fire"

# Hidden layer: two neurons look at the same inputs from different angles.
HIDDEN_NEURONS = (
    ((0.9, 0.1, 0.1), -4.0),   # neuron A cares mostly about the weather
    ((0.1, 0.6, 0.6), -3.0),   # neuron B cares mostly about time and energy
)
OUTPUT_NEURON = ((0.6, 0.6), -1.0)     # fires only if BOTH hidden neurons fire
MAX_INPUT_TRIES = 3


def step_activation(total):
    """Activation function: output 1 if the total is above 0, otherwise 0."""
    return 1 if total > 0 else 0


def perceptron(inputs, weights, bias):
    """One artificial neuron. Returns (weighted_sum, total_with_bias, output).

    inputs x weights -> add them up -> add bias -> activation function -> output.
    """
    weighted_sum = sum(weight * value for weight, value in zip(weights, inputs))
    total = weighted_sum + bias
    return weighted_sum, total, step_activation(total)


def two_layer_forward(inputs):
    """Forward propagation through a hidden layer and an output neuron.

    Returns (hidden_outputs, final_output). Each hidden neuron reads the user's
    inputs; the output neuron reads the hidden neurons' outputs.
    """
    hidden_outputs = [perceptron(inputs, weights, bias)[2] for weights, bias in HIDDEN_NEURONS]
    output_weights, output_bias = OUTPUT_NEURON
    final_output = perceptron(hidden_outputs, output_weights, output_bias)[2]
    return hidden_outputs, final_output


def read_number(prompt, input_fn=input, print_fn=print):
    """Ask for a number; re-ask on bad input. Returns None if the user gives up."""
    for _ in range(MAX_INPUT_TRIES):
        raw = input_fn(prompt).strip().lower()
        if raw == "cancel":
            return None
        try:
            value = float(raw)
        except ValueError:
            value = None
        if value is not None and math.isfinite(value):
            return value
        print_fn("Assistant: Please type a number (for example 7), or 'cancel' to stop.")
    return None


def _show(value):
    """Format a number compactly: 8.0 -> '8', 3.2 -> '3.2'."""
    return f"{value:g}"


def perceptron_demo(name, input_fn=input, print_fn=print):
    """Interactive walk-through of a perceptron followed by a tiny layered network."""
    print_fn(f"Assistant: {name}, let's see an artificial neuron decide: 'Should I go for a walk?'")
    print_fn("Assistant: I'll ask for 3 inputs. My weights and bias are fixed (nothing is trained).")
    inputs = []
    for prompt in INPUT_PROMPTS:
        value = read_number(prompt, input_fn, print_fn)
        if value is None:
            return "No problem, we can try the perceptron another time."
        inputs.append(value)

    weighted_sum, total, output = perceptron(inputs, PERCEPTRON_WEIGHTS, PERCEPTRON_BIAS)
    terms = " + ".join(f"{_show(weight)}*{_show(number)}"
                       for weight, number in zip(PERCEPTRON_WEIGHTS, inputs))
    print_fn("Assistant: --- Single neuron (perceptron) ---")
    labelled = ", ".join(f"{label}={_show(number)}" for label, number in zip(INPUT_NAMES, inputs))
    print_fn(f"  Inputs      : {labelled}")
    print_fn(f"  Weighted sum: {terms} = {_show(round(weighted_sum, 4))}")
    print_fn(f"  Add bias    : {_show(round(weighted_sum, 4))} + ({_show(PERCEPTRON_BIAS)}) = {_show(round(total, 4))}")
    print_fn(f"  Activation  : step function (sum > 0 -> 1, else 0) gives output {output}")

    hidden_outputs, final_output = two_layer_forward(inputs)
    print_fn("Assistant: --- Layering: a hidden layer feeding an output neuron ---")
    print_fn(f"  Hidden neuron A (weather-focused)      -> {hidden_outputs[0]}")
    print_fn(f"  Hidden neuron B (time/energy-focused)  -> {hidden_outputs[1]}")
    print_fn(f"  Output neuron (needs both to fire)     -> {final_output}")

    verdict = "Yes, go for a walk!" if output == 1 else "Maybe skip the walk today."
    return (f"Output {output} = {verdict} This one neuron is the building block of every "
            "neural network, going back to the perceptron of the 1950s.")


# ---------------------------------------------------------------------------
# Plain-language explanation of how the project maps to AI, ML and DL
# ---------------------------------------------------------------------------

def explain_concepts():
    """Short tour of the AI / ML / DL ideas demonstrated by this assistant."""
    return (
        "Here is how I demonstrate the big ideas:\n"
        "  AI (rule-based): I read your text, detect keywords such as 'joke' or 'time', and follow\n"
        "      if/elif rules to pick a response. Try any command.\n"
        "  ML (analogies, nothing is trained): type 'recommend' to see rules classify the time of\n"
        "      day like a decision tree, and 'stats' to see me learn your preferences from this session.\n"
        "  DL (building blocks): type 'perceptron' to watch inputs, weights, a bias and an\n"
        "      activation function produce an output, then pass through a hidden layer."
    )
