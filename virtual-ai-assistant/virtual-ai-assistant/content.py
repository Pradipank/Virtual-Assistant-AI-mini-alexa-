"""Quotes, jokes and facts (FR-06, FR-07, FR-08).

Each feature is just a Python list of strings. The ``random`` module picks one
entry per request. The previous pick is excluded so the same item is never
served twice in a row.
"""

import random

QUOTES = [
    "Every expert was once a beginner.",
    "Small steps every day lead to big results.",
    "Mistakes are proof that you are trying.",
    "Progress, not perfection.",
    "Debugging is just learning in disguise.",
    "The best way to learn to code is to write code.",
    "Difficult roads often lead to beautiful destinations.",
    "Don't watch the clock; do what it does \u2014 keep going.",
]

JOKES = [
    "Why did the developer go broke? Because they used up all their cache.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the neural network go to school? To improve its training.",
    "There are 10 kinds of people: those who understand binary and those who don't.",
    "Why was the computer cold? It left its Windows open.",
    "A SQL query walks into a bar, sees two tables and asks: 'Can I join you?'",
    "Why did the function break up with the loop? It needed some space to return.",
    "I would tell you a UDP joke, but you might not get it.",
]

FACTS = [
    "The term 'artificial intelligence' was coined at a 1956 workshop at Dartmouth College.",
    "The perceptron, an early artificial neuron, was introduced by Frank Rosenblatt in 1958.",
    "Python is named after the comedy group Monty Python, not the snake.",
    "The first computer 'bug' was a real moth found in a Harvard computer in 1947.",
    "The word 'robot' comes from a Czech word meaning forced labour, from a 1920 play.",
    "IBM's Deep Blue defeated chess champion Garry Kasparov in 1997.",
    "Alan Turing proposed his famous 'imitation game' test of machine intelligence in 1950.",
    "'Deep' in deep learning refers to the number of layers in a neural network.",
]

_last_served = {}   # category name -> last item shown (session memory)


def pick_random(items, previous=None):
    """Choose a random item, avoiding ``previous`` when there is more than one choice."""
    if len(items) > 1 and previous in items:
        candidates = [item for item in items if item != previous]
    else:
        candidates = items
    return random.choice(candidates)


def _serve(category, items):
    """Pick an item for a category and remember it as the last one served."""
    selected = pick_random(items, _last_served.get(category))
    _last_served[category] = selected
    return selected


def get_random_quote():
    """Return a random motivational quote (FR-06)."""
    return _serve("quote", QUOTES)


def get_random_joke():
    """Return a random joke (FR-07)."""
    return _serve("joke", JOKES)


def get_random_fact():
    """Return a random fact (FR-08)."""
    return _serve("fact", FACTS)
