"""Date and time reporting (FR-03, FR-04).

Uses only the built-in ``datetime`` module. Every function accepts an optional
``now`` value so the output can be tested with a fixed moment in time.
"""

from datetime import datetime


def get_current_time(now=None):
    """Return a friendly sentence with the current time, e.g. "It's currently 3:45 PM."."""
    moment = now or datetime.now()
    # %I gives "03"; lstrip("0") turns it into "3" so the sentence reads naturally.
    return f"It's currently {moment.strftime('%I:%M %p').lstrip('0')}."


def get_current_date(now=None):
    """Return a friendly sentence with today's date, e.g. "Today is Thursday, 08 October 2026."."""
    moment = now or datetime.now()
    return f"Today is {moment.strftime('%A, %d %B %Y')}."


def get_current_hour(now=None):
    """Return the current hour (0-23). Used by the rule-based recommendation demo."""
    moment = now or datetime.now()
    return moment.hour
