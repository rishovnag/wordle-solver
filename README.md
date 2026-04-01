# WordleSolver

A Python implementation of the classic Wordle word-guessing game, bundled with intelligent solver/helper tools. Play the game through a graphical interface, or use the helper tools (CLI or GUI) to get optimal word suggestions while playing Wordle elsewhere.

## Features

**Wordle Game** — A fully playable Wordle clone with a dark-themed tkinter GUI. Guess a hidden 5-letter word in 6 attempts, with color-coded feedback (green, yellow, gray) after each guess. Includes reset and new-game controls.

**Wordle Helper (CLI)** — A terminal-based assistant. Enter your guesses and the color feedback you received, and the helper narrows down the candidate word list and suggests optimal next guesses ranked by letter-frequency scoring.

**Wordle Helper (GUI)** — The same constraint-solving logic as the CLI helper, wrapped in a tkinter interface. Type your guess, click each letter tile to cycle through green/yellow/gray, and submit to see ranked suggestions and a running guess history.

## Project Structure

```
WordleSolver/
├── main.py                 # Entry point — menu to launch any mode
├── wordle_game.py          # Playable Wordle game (tkinter GUI)
├── wordle_helper.py        # CLI-based Wordle solver/helper
├── wordle_helper_gui.py    # GUI-based Wordle solver/helper (tkinter)
├── dictionary_manager.py   # Shared dictionary loader and word filtering
├── words.txt               # Dictionary of 5,758 five-letter words
├── requirements.txt        # Dependencies (stdlib only)
└── .gitignore
```

## Requirements

- Python 3.10 or later
- tkinter (included with most Python installations)

If tkinter is not installed:

- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **Fedora:** `sudo dnf install python3-tkinter`
- **macOS:** Included with the official Python installer from python.org

No external packages are needed — the project uses only the Python standard library.

## Getting Started

### Run via the main menu

```bash
python main.py
```

You'll be prompted to choose between the three modes (game, CLI helper, or GUI helper).

### Run a specific module directly

```bash
# Play the Wordle game
python wordle_game.py

# Use the CLI helper
python wordle_helper.py

# Use the GUI helper
python wordle_helper_gui.py
```

## How to Play (Wordle Game)

1. Launch the game. A random 5-letter target word is chosen.
2. Type a 5-letter word using your keyboard and press **Enter**.
3. Each tile changes color:
   - **Green** — correct letter in the correct position
   - **Yellow** — correct letter in the wrong position
   - **Gray** — letter is not in the word
4. You have 6 attempts to guess the word.
5. Use **Backspace** to delete letters, **Reset Game** to retry the same word, or **New Game** to pick a fresh word.

## How to Use the Helper

### CLI Helper

1. Run `python wordle_helper.py`.
2. Enter the 5-letter word you guessed in your external Wordle game.
3. Enter the color feedback as a 5-character string: `g` = green, `y` = yellow, `x` = gray. For example, if you guessed CRANE and got green-gray-yellow-gray-green, enter `gxygxg` — wait, that's 6 chars. Enter `gxyxg`.
4. The helper displays the top 5 suggested words for your next guess.
5. Repeat for up to 5 rounds, or type `exit` to quit.

### GUI Helper

1. Run `python wordle_helper_gui.py`.
2. Type your 5-letter guess in the input field.
3. Click each letter button to cycle its color (default → green → yellow → gray → default).
4. Click **Submit Guess**.
5. View ranked suggestions in the bottom panel and your guess history in the middle panel.
6. Click **Reset Game** to start over.

## How the Solver Works

The solver uses a **letter-frequency scoring** algorithm to rank candidate words:

1. After each guess, positional constraints (green, yellow, gray) are recorded.
2. The full dictionary is filtered down to words satisfying all constraints.
3. Each remaining word is scored by summing the relative frequency of its unique letters across the remaining candidate pool.
4. A penalty is applied for duplicate letters (words with all unique letters are preferred early on since they reveal more information).
5. The top-scoring words are presented as suggestions.

## Dictionary

The included `words.txt` contains 5,758 valid 5-letter English words. The dictionary manager also filters these down to an "answer pool" of 5,345 words by excluding words with very rare letters (Q, X, Z), words with multiple uncommon letters, and words where any single letter appears more than twice — ensuring fair and enjoyable gameplay.

If `words.txt` is not found at runtime, a built-in fallback list of common words is used automatically.

## License

This project is provided as-is for educational and personal use.
