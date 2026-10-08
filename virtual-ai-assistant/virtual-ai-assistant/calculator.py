"""Basic calculator (FR-05).

Parses a command such as "calculate 12 + 8" into two numbers and an operator,
performs the operation, and reports friendly errors instead of crashing.
"""

import math
import re

# Spoken operators are converted to symbols so "5 plus 3" works like "5 + 3".
WORD_OPERATORS = (
    ("multiplied by", "*"),
    ("divided by", "/"),
    ("times", "*"),
    ("plus", "+"),
    ("minus", "-"),
)
# Words that introduce a calculation but carry no numbers.
FILLER_WORDS = ("calculate", "calc", "compute", "what is", "what's", "whats")
USAGE_MESSAGE = "I need two numbers and an operator, like: calculate 12 + 8"
DIVIDE_BY_ZERO_MESSAGE = "I can't divide by zero \u2014 try a different number."
OVERFLOW_MESSAGE = "That number is too big for me to handle. Try smaller numbers."
DISPLAY_DECIMALS = 4

# number, operator (+ - * / or the letter x), number
EXPRESSION_PATTERN = re.compile(r"^(-?\d+(?:\.\d+)?)\s*([+\-*/x])\s*(-?\d+(?:\.\d+)?)$")


def parse_expression(text):
    """Turn text into (left, symbol, right). Raises ValueError with a friendly message."""
    cleaned = text.lower()
    for word, symbol in WORD_OPERATORS:
        cleaned = re.sub(rf"\b{re.escape(word)}\b", f" {symbol} ", cleaned)
    for filler in FILLER_WORDS:
        cleaned = re.sub(rf"\b{re.escape(filler)}\b", " ", cleaned)
    cleaned = cleaned.replace("?", " ").replace("=", " ").strip()
    match = EXPRESSION_PATTERN.match(cleaned)
    if match is None:
        raise ValueError(USAGE_MESSAGE)
    left, symbol, right = match.groups()
    return float(left), symbol, float(right)


def calculate(left, symbol, right):
    """Apply one arithmetic operator. Raises ZeroDivisionError or OverflowError."""
    if symbol == "+":
        result = left + right
    elif symbol == "-":
        result = left - right
    elif symbol in ("*", "x"):
        result = left * right
    elif symbol == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        result = left / right
    else:
        raise ValueError(USAGE_MESSAGE)
    if not math.isfinite(result):
        raise OverflowError("result too large")
    return result


def format_number(value):
    """Show whole numbers without '.0' (20.0 -> '20') and round long decimals."""
    if value == int(value):
        return str(int(value))
    return str(round(value, DISPLAY_DECIMALS))


def looks_like_math(text):
    """True if the text contains a valid 'number operator number' expression."""
    try:
        parse_expression(text)
    except ValueError:
        return False
    return True


def run_calculation(text):
    """Parse and solve the user's request. Always returns a message, never crashes."""
    try:
        left, symbol, right = parse_expression(text)
        result = calculate(left, symbol, right)
    except ZeroDivisionError:
        return DIVIDE_BY_ZERO_MESSAGE
    except OverflowError:
        return OVERFLOW_MESSAGE
    except ValueError as error:
        return str(error)
    return f"The result is {format_number(result)}"
