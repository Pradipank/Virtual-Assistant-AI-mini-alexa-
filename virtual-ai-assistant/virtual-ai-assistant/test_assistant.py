"""Automated tests mapped to the PRD testing checklist (section 33) and
acceptance criteria (section 30). Uses only the standard library.

Run with:  python -m unittest -v
"""

import ast
import glob
import os
import unittest
from datetime import datetime

import ai_concepts
import calculator
import content
import datetime_utils
import game
import greetings
import help_menu
import main

BANNED_LIBRARIES = {"tensorflow", "torch", "keras", "sklearn", "cv2", "pandas", "numpy",
                    "requests", "openai", "google", "urllib", "socket", "sqlite3", "pymongo"}


def run_session(lines):
    """Run the whole assistant with scripted input; return everything it printed."""
    remaining = list(lines)
    printed = []

    def fake_input(_prompt=""):
        if not remaining:
            raise EOFError
        return remaining.pop(0)

    main.run_assistant(fake_input, printed.append)
    return "\n".join(printed)


def scripted(lines):
    """Return an input function that feeds ``lines`` one by one."""
    queue = list(lines)

    def fake_input(_prompt=""):
        if not queue:
            raise EOFError
        return queue.pop(0)

    return fake_input


class TestGreetingAndSession(unittest.TestCase):
    def test_name_requested_and_reused(self):
        output = run_session(["priya", "hello", "thanks", "exit"])
        self.assertIn("What's your name?", output)
        self.assertGreaterEqual(output.count("Priya"), 2)      # FR-01 / FR-02

    def test_name_cleaning(self):
        self.assertEqual(greetings.clean_name("  my name is  priya "), "Priya")

    def test_blank_names_fall_back_to_default(self):
        name = greetings.get_user_name(scripted(["", "123", "!!"]), lambda _msg: None)
        self.assertEqual(name, greetings.DEFAULT_NAME)

    def test_rename(self):
        output = run_session(["sam", "my name is Alex", "what is my name", "exit"])
        self.assertIn("Alex", output)


class TestDateTime(unittest.TestCase):
    def test_time_and_date_format(self):
        fixed = datetime(2026, 10, 8, 15, 45)
        self.assertEqual(datetime_utils.get_current_time(fixed), "It's currently 3:45 PM.")
        self.assertEqual(datetime_utils.get_current_date(fixed), "Today is Thursday, 08 October 2026.")

    def test_commands_return_current_values(self):
        output = run_session(["sam", "date", "time", "exit"])
        self.assertIn(datetime.now().strftime("%Y"), output)
        self.assertIn("It's currently", output)


class TestCalculator(unittest.TestCase):
    def test_all_operators(self):
        self.assertEqual(calculator.run_calculation("calculate 12 + 8"), "The result is 20")
        self.assertEqual(calculator.run_calculation("calculate 12 - 8"), "The result is 4")
        self.assertEqual(calculator.run_calculation("calculate 12 * 8"), "The result is 96")
        self.assertEqual(calculator.run_calculation("calculate 12 / 8"), "The result is 1.5")

    def test_spoken_operators_and_decimals(self):
        self.assertEqual(calculator.run_calculation("what is 5 plus 3"), "The result is 8")
        self.assertEqual(calculator.run_calculation("calculate 2.5 times 4"), "The result is 10")

    def test_divide_by_zero(self):
        self.assertEqual(calculator.run_calculation("calculate 5 / 0"),
                         "I can't divide by zero \u2014 try a different number.")

    def test_non_numeric_input(self):
        for bad in ("calculate abc + 2", "calculate", "calculate 5 +", "calculate 1 + 2 + 3"):
            self.assertIn("two numbers", calculator.run_calculation(bad))

    def test_huge_numbers_do_not_crash(self):
        self.assertIn("too big", calculator.run_calculation("calculate " + "9" * 400 + " * " + "9" * 400))


class TestContent(unittest.TestCase):
    def test_randomness(self):
        for getter in (content.get_random_joke, content.get_random_quote, content.get_random_fact):
            results = {getter() for _ in range(10)}
            self.assertGreaterEqual(len(results), 2)

    def test_no_immediate_repeat(self):
        previous = content.get_random_joke()
        for _ in range(30):
            current = content.get_random_joke()
            self.assertNotEqual(previous, current)
            previous = current


class TestGame(unittest.TestCase):
    def test_hints_and_win(self):
        printed = []
        result = game.play_guessing_game("Sam", scripted(["5", "15", "10"]), printed.append, secret=10)
        self.assertIn("got it in 3 tries", result)
        self.assertTrue(any("Higher!" in line for line in printed))
        self.assertTrue(any("Lower!" in line for line in printed))

    def test_attempt_limit_enforced(self):
        printed = []
        result = game.play_guessing_game("Sam", scripted(["1"] * 10), printed.append, secret=10)
        self.assertIn("Out of tries", result)
        self.assertEqual(sum(1 for line in printed if "Higher!" in line), game.MAX_ATTEMPTS - 1)

    def test_invalid_input_does_not_use_attempts(self):
        result = game.play_guessing_game("Sam", scripted(["abc", "99", "10"]), lambda _msg: None, secret=10)
        self.assertIn("got it in 1 try", result)

    def test_quit_and_endless_invalid_input(self):
        self.assertIn("cancelled", game.play_guessing_game("Sam", scripted(["quit"]), lambda _m: None, secret=7))
        endless = game.play_guessing_game("Sam", scripted(["x"] * 20), lambda _m: None, secret=7)
        self.assertIn("stop the game", endless)


class TestHelpAndFallback(unittest.TestCase):
    def test_help_lists_every_command(self):
        text = help_menu.format_help()
        for command, _description in help_menu.COMMANDS:
            self.assertIn(command, text)

    def test_unknown_input_gives_fallback_and_continues(self):
        output = run_session(["sam", "asdkfj", "time", "exit"])
        self.assertIn("I'm not sure I understood that", output)
        self.assertIn("It's currently", output)            # loop kept running

    def test_exit_variants(self):
        for word in ("exit", "quit", "bye"):
            self.assertIn("Goodbye, Sam!", run_session(["sam", word]))

    def test_ctrl_d_ends_cleanly(self):
        self.assertIn("Goodbye", run_session(["sam"]))


class TestAIConcepts(unittest.TestCase):
    def test_recommendation_changes_with_time(self):
        categories = {ai_concepts.recommend_activity(hour)[0] for hour in range(24)}
        self.assertGreaterEqual(len(categories), 8)
        self.assertNotEqual(ai_concepts.recommend_activity(3)[0], ai_concepts.recommend_activity(12)[0])

    def test_every_hour_is_covered_and_bad_hours_rejected(self):
        for hour in range(24):
            category, advice = ai_concepts.recommend_activity(hour)
            self.assertTrue(category and advice)
        for bad_hour in (-1, 24):
            with self.assertRaises(ValueError):
                ai_concepts.recommend_activity(bad_hour)

    def test_hour_extraction(self):
        self.assertEqual(ai_concepts.extract_hour("recommend at 9"), 9)
        self.assertEqual(ai_concepts.extract_hour("suggest 7 pm"), 19)
        self.assertEqual(ai_concepts.extract_hour("recommend 12 am"), 0)
        self.assertIsNone(ai_concepts.extract_hour("recommend something"))

    def test_perceptron_outputs_zero_or_one(self):
        _, _, high = ai_concepts.perceptron([8, 2, 6], ai_concepts.PERCEPTRON_WEIGHTS, ai_concepts.PERCEPTRON_BIAS)
        _, _, low = ai_concepts.perceptron([2, 0, 3], ai_concepts.PERCEPTRON_WEIGHTS, ai_concepts.PERCEPTRON_BIAS)
        self.assertEqual((high, low), (1, 0))

    def test_layered_network(self):
        self.assertEqual(ai_concepts.two_layer_forward([8, 2, 6])[1], 1)
        self.assertEqual(ai_concepts.two_layer_forward([9, 0, 1])[1], 0)

    def test_perceptron_demo_handles_bad_input(self):
        result = ai_concepts.perceptron_demo("Sam", scripted(["x", "y", "z"]), lambda _m: None)
        self.assertIn("another time", result)
        output = run_session(["sam", "perceptron", "8", "2", "6", "exit"])
        self.assertIn("gives output 1", output)

    def test_preferences_learned_from_session(self):
        output = run_session(["sam", "joke", "joke", "fact", "stats", "exit"])
        self.assertIn("jokes 2 times", output)
        self.assertIn("haven't learned", run_session(["sam", "stats", "exit"]))


class TestRobustness(unittest.TestCase):
    def test_twenty_plus_odd_inputs_never_crash(self):
        odd_inputs = ["", "   ", "???", "asdkfj", "12345", "calculate", "calculate 5 /", "calc 1 +",
                      "recommend 99", "recommend at -5", "my name is", "my name is 123", "game",
                      "q", "stop", "perceptron", "cancel", "x", "HELP", "Time!!", "JoKe", "ai", "bye"]
        output = run_session(["sam"] + odd_inputs)
        self.assertIn("Assistant:", output)
        self.assertNotIn("Traceback", output)

    def test_intent_detection_examples(self):
        expected = {"what time is it": "time", "tell me a joke": "joke", "what is 5 plus 3": "calculate",
                    "give me a quote": "quote", "play a game": "game", "what should i do now": "recommend",
                    "good morning": "greeting", "who are you": "about", "sometimes": None}
        for text, intent in expected.items():
            self.assertEqual(main.detect_intent(text), intent, text)


class TestProjectRules(unittest.TestCase):
    def test_no_disallowed_libraries(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        for path in glob.glob(os.path.join(folder, "*.py")):
            with open(path, encoding="utf-8") as source_file:
                tree = ast.parse(source_file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported = {alias.name.split(".")[0] for alias in node.names}
                elif isinstance(node, ast.ImportFrom):
                    imported = {(node.module or "").split(".")[0]}
                else:
                    continue
                self.assertFalse(imported & BANNED_LIBRARIES, f"{path} imports {imported}")


if __name__ == "__main__":
    unittest.main()
