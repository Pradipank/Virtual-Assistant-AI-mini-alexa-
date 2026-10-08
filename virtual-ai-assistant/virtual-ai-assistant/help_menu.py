"""Help menu (FR-10). The command list lives in ONE place so help can never drift."""

# (command as typed, description)
COMMANDS = [
    ("hello", "say hi to me"),
    ("time", "show the current time"),
    ("date", "show the current date"),
    ("calculate 12 + 8", "do a calculation (+, -, *, /)"),
    ("joke", "tell a joke"),
    ("quote", "motivational quote"),
    ("fact", "random fact"),
    ("game", "play the number guessing game"),
    ("recommend [hour]", "rule-based activity suggestion, e.g. 'recommend 15'"),
    ("perceptron", "watch an artificial neuron make a decision"),
    ("concepts", "how I demonstrate AI, ML and DL"),
    ("stats", "what I've learned about your favourites"),
    ("my name is <name>", "change the name I call you"),
    ("help", "show this menu"),
    ("exit", "quit the assistant (also: quit, bye)"),
]
COLUMN_WIDTH = 20


def format_help():
    """Build the help text as a single string."""
    lines = ["Here's what I can do:"]
    for command, description in COMMANDS:
        lines.append(f"  - {command:<{COLUMN_WIDTH}} {description}")
    return "\n".join(lines)


def print_help(print_fn=print):
    """Print the help menu."""
    print_fn(format_help())
