# Virtual AI Assistant (Mini Alexa)

**Nexbridge Technologies - AI Internship Program, Project 1 (AI-INT-P1-VAA)**

A text-based, rule-based virtual assistant that runs entirely offline in the terminal.
It uses **only the Python standard library**: no datasets, APIs, databases, or ML frameworks.
AI, ML and DL ideas are shown through plain Python arithmetic and if/elif logic, **nothing is trained**.

## Requirements

- Python 3.8 or newer (check with `python --version`, or `python3 --version` on Mac/Linux)
- A terminal and any text editor (VS Code recommended). No `pip install` needed.

## How to run

```
cd virtual-ai-assistant
python main.py
```

Run the automated tests with `python -m unittest -v`.

## Commands

| Command | What it does |
| --- | --- |
| `hello` | Greets you by name |
| `time` / `date` | Current time / date |
| `calculate 12 + 8` | Arithmetic with `+ - * /` (also "5 plus 3", "6 times 7") |
| `joke` / `quote` / `fact` | Random item from a predefined list |
| `game` | Number guessing game (1-20, 5 tries, higher/lower hints) |
| `recommend [hour]` | Rule-based activity suggestion, e.g. `recommend 15` or `recommend 7 pm` |
| `perceptron` | Watch an artificial neuron (and a tiny hidden layer) decide |
| `concepts` | Explains how the project demonstrates AI, ML and DL |
| `stats` | What the assistant "learned" about your favourites this session |
| `my name is <name>` | Change the name used for you |
| `help` | Lists every command |
| `exit` / `quit` / `bye` | Ends the session |

## Project structure

```
virtual-ai-assistant/
|-- main.py            entry point, main loop, intent detection and routing
|-- greetings.py       name capture and small-talk replies
|-- datetime_utils.py  date and time
|-- calculator.py      expression parsing and arithmetic
|-- content.py         QUOTES / JOKES / FACTS lists and random selection
|-- game.py            number guessing game
|-- ai_concepts.py     rule-based recommendation, perceptron, layered demo, preferences
|-- help_menu.py       single source of truth for the command list
|-- test_assistant.py  automated tests (standard library `unittest`)
`-- README.md
```

## How it works

Every loop iteration follows the PRD workflow:

```
input -> normalize (lowercase, trim) -> keyword/pattern match -> respond_*() -> print -> loop
```

`detect_intent()` in `main.py` scores each intent by how many of its keywords appear in the
text and picks the best match (a simple *similarity match*). `route()` then calls the matching
`respond_*()` function. Unknown input returns a friendly fallback; invalid input never crashes
the program.

## Requirement coverage (FR-01 to FR-14)

| ID | Where it is implemented |
| --- | --- |
| FR-01 / FR-02 | `greetings.get_user_name()`, name stored in the session and reused in greetings, game, recommendation, perceptron demo and goodbye |
| FR-03 / FR-04 | `datetime_utils.get_current_date()` / `get_current_time()` |
| FR-05 | `calculator.parse_expression()`, `calculate()`, `run_calculation()` (divide-by-zero and bad input handled with `try/except`) |
| FR-06 / 07 / 08 | `content.get_random_quote()` / `get_random_joke()` / `get_random_fact()` |
| FR-09 | `game.play_guessing_game()` (5 attempts, higher/lower hints) |
| FR-10 | `help_menu.format_help()` |
| FR-11 | `main.end_session()` for `exit`, `quit`, `bye` |
| FR-12 | `FALLBACK_MESSAGE` in `main.py` |
| FR-13 | `ai_concepts.recommend_activity()` (if/elif chain on the hour) |
| FR-14 | `ai_concepts.perceptron()`, `perceptron_demo()`, `two_layer_forward()` |

## AI, ML and DL concepts in the code

**Artificial Intelligence (rule-based systems)**
- *Rule-based system, keyword detection, pattern matching, intent recognition:* `INTENT_RULES` and `detect_intent()` in `main.py`.
- *Human-computer interaction:* the input -> process -> respond loop in `run_assistant()`.
- *Intelligent decision-making:* `recommend_activity()` chooses an output from many conditional branches.

**Machine Learning (analogies only, no training)**
- *Classification and decision-tree logic:* `recommend_activity()`. The hour is the input feature, each `elif` is a split, and the returned category is the "predicted label".
- *Predicting simple outcomes / recommendation logic:* the same function, plus the random-selection features in `content.py`.
- *Learning preferences during execution:* the stored name, and `summarize_preferences()` which counts which features you use.
- *Similarity matching:* keyword-overlap scoring in `detect_intent()`.

**Deep Learning (building blocks, fixed weights)**
- *Artificial neuron / perceptron:* `perceptron()` takes **inputs**, multiplies by fixed **weights**, adds a **bias**, and applies a step **activation function** to give an **output** of 0 or 1.
- *Forward propagation:* the demo prints each step from inputs to output.
- *Hidden layer:* `two_layer_forward()` feeds two hidden neurons' outputs into an output neuron.

## Testing

`python -m unittest -v` runs 31 tests covering every item in the PRD testing checklist.

| Checklist item | Verified by |
| --- | --- |
| Starts without errors; exit ends cleanly | `TestHelpAndFallback.test_exit_variants`, `test_ctrl_d_ends_cleanly` |
| Name requested and reused | `TestGreetingAndSession` |
| Date and time correct | `TestDateTime` |
| `+ - * /`, divide by zero, non-numeric input | `TestCalculator` |
| Joke/quote/fact vary across repeats | `TestContent` |
| Guessing game limit and higher/lower feedback | `TestGame` |
| Help lists every command | `test_help_lists_every_command` |
| Unknown input gives fallback, no crash (20+ odd inputs) | `TestRobustness` |
| Recommendation differs by time of day | `TestAIConcepts.test_recommendation_changes_with_time` |
| Perceptron output is 0 or 1 | `test_perceptron_outputs_zero_or_one` |
| No disallowed libraries | `TestProjectRules` |

Sample inputs and outputs (from PRD section 34):

| Input | Output |
| --- | --- |
| `calculate 12 + 8` | The result is 20 |
| `calculate 5 / 0` | I can't divide by zero - try a different number. |
| `time` | It's currently 3:45 PM. |
| `game` | I'm thinking of a number between 1 and 20. You have 5 tries. Guess a number: |
| `asdkfj` | I'm not sure I understood that - type 'help' to see what I can do. |
| `exit` | Goodbye, Priya! Have a great day. |

## Known limitations (by design)

- Keyword matching is literal. Some reasonable phrasings fall through to the fallback message. This is an accepted limitation of a rule-based system and a good discussion point for mentor review.
- All state lives in memory and resets on restart. There is no voice, GUI, network or file storage.

## Code walkthrough points for mentor review

1. Follow one command (`joke`) from `input()` through `normalize` -> `detect_intent` -> `route` -> `respond_joke` -> `content.get_random_joke`.
2. Explain why `recommend_activity()` is a hand-written decision tree and how a trained classifier would differ (it would learn the splits from data).
3. Walk through `perceptron()` with real numbers and explain what weights and bias do.
4. Show how errors are handled (`calculator.run_calculation`, `game` invalid input, `read_number`).
