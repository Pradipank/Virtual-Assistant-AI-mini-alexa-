"""Number guessing game (FR-09)."""

import random

LOW_NUMBER = 1
HIGH_NUMBER = 20
MAX_ATTEMPTS = 5              # the attempt limit required by FR-09
MAX_INVALID_INPUTS = 5        # stops the game if the user keeps typing non-numbers
QUIT_WORDS = ("quit", "exit", "stop", "cancel")


def play_guessing_game(name, input_fn=input, print_fn=print,
                       secret=None, max_attempts=MAX_ATTEMPTS):
    """Run one game and return the closing message.

    ``secret`` can be supplied for testing; otherwise ``random.randint`` picks it.
    Invalid input (letters, out-of-range numbers) does not use up an attempt.
    """
    if secret is None:
        secret = random.randint(LOW_NUMBER, HIGH_NUMBER)
    print_fn(f"Assistant: I'm thinking of a number between {LOW_NUMBER} and {HIGH_NUMBER}. "
             f"You have {max_attempts} tries.")

    attempts_used = 0
    invalid_inputs = 0
    while attempts_used < max_attempts:
        raw = input_fn("Guess a number: ").strip().lower()
        if raw in QUIT_WORDS:
            return f"Game cancelled. The number was {secret}."
        try:
            guess = int(raw)
        except ValueError:
            guess = None
        if guess is None or not LOW_NUMBER <= guess <= HIGH_NUMBER:
            invalid_inputs += 1
            if invalid_inputs >= MAX_INVALID_INPUTS:
                return f"Let's stop the game for now. The number was {secret}."
            print_fn(f"Assistant: Please enter a whole number from {LOW_NUMBER} to {HIGH_NUMBER}.")
            continue

        attempts_used += 1
        if guess == secret:
            return f"You got it in {attempts_used} {'try' if attempts_used == 1 else 'tries'}, {name}!"
        hint = "Higher!" if guess < secret else "Lower!"
        tries_left = max_attempts - attempts_used
        if tries_left > 0:
            print_fn(f"Assistant: {hint} You have {tries_left} {'try' if tries_left == 1 else 'tries'} left.")

    return f"Out of tries! The number was {secret}. Better luck next time, {name}."
