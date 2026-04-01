"""
WordleHelperGUI: A tkinter GUI application to help you play Wordle.
Enter your 5-letter guess and click on letters to set their colors,
then get suggestions for your next guess.
Ported from the Java Swing WordleHelperGUI.java.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
from collections import Counter
from dataclasses import dataclass


# --- Constants ---
WORD_LENGTH = 5
GREEN = 'g'
YELLOW = 'y'
GRAY = 'x'

# --- Colors ---
GREEN_COLOR = "#6aaa64"
YELLOW_COLOR = "#c9b458"
GRAY_COLOR = "#787c7e"
DEFAULT_COLOR = "#d3d6da"
TEXT_COLOR = "#ffffff"
BLACK = "#000000"


@dataclass(frozen=True)
class Constraint:
    letter: str
    position: int
    colour: str


class WordleHelperGUI:
    def __init__(self):
        self.possible_words: set[str] = self._load_words()
        self.letters_in_word: set[str] = set()
        self.letters_not_in_word: set[str] = set()
        self.constraint_list: list[Constraint] = []
        self.already_guessed: list[str] = []
        self.current_guess = 0

        # Track current color state per button: 'default', 'green', 'yellow', 'gray'
        self.button_colors: list[str] = ['default'] * WORD_LENGTH

        self.root = tk.Tk()
        self.root.title("Wordle Helper")
        self.root.configure(bg="white")
        self.root.minsize(600, 700)

        self._init_gui()
        self._update_suggestions()

    def _init_gui(self) -> None:
        # --- Header ---
        header = tk.Frame(self.root, bg="white", padx=10, pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header, text="Wordle Helper", font=("Arial", 24, "bold"),
            fg="#787c7e", bg="white",
        ).pack()

        tk.Label(
            header,
            text="Enter your 5-letter guess and click each letter to cycle through colors:\n"
                 "Green (correct position) | Yellow (wrong position) | Gray (not in word)",
            font=("Arial", 11), bg="white", justify=tk.CENTER,
        ).pack(pady=(5, 0))

        # --- Input Panel ---
        input_frame = tk.LabelFrame(self.root, text="Current Guess", bg="white", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        word_row = tk.Frame(input_frame, bg="white")
        word_row.pack()
        tk.Label(word_row, text="Enter word:", bg="white").pack(side=tk.LEFT, padx=5)
        self.word_input = tk.Entry(word_row, font=("Arial", 16, "bold"), width=8)
        self.word_input.pack(side=tk.LEFT, padx=5)
        self.word_input.bind("<Return>", lambda e: self._process_guess())

        # Letter buttons
        letters_frame = tk.Frame(input_frame, bg="white")
        letters_frame.pack(pady=10)

        self.letter_buttons: list[tk.Button] = []
        for i in range(WORD_LENGTH):
            btn = tk.Button(
                letters_frame, text="-", width=3, height=1,
                font=("Arial", 20, "bold"), bg=DEFAULT_COLOR, fg=BLACK,
                relief="solid", borderwidth=2,
                command=lambda pos=i: self._cycle_letter_color(pos),
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.letter_buttons.append(btn)

        # Submit button
        submit_btn = tk.Button(
            input_frame, text="Submit Guess", font=("Arial", 14, "bold"),
            bg="#538d4e", fg="white", command=self._process_guess,
        )
        submit_btn.pack(pady=5)

        # --- Guess History ---
        history_frame = tk.LabelFrame(self.root, text="Guess History", bg="white", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.history_canvas = tk.Canvas(history_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_canvas.yview)
        self.history_inner = tk.Frame(self.history_canvas, bg="white")

        self.history_inner.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all")),
        )
        self.history_canvas.create_window((0, 0), window=self.history_inner, anchor="nw")
        self.history_canvas.configure(yscrollcommand=scrollbar.set)

        self.history_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Bottom Panel ---
        bottom = tk.Frame(self.root, bg="white", padx=10, pady=10)
        bottom.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Ready to start! Enter your first guess.")
        tk.Label(
            bottom, textvariable=self.status_var,
            font=("Arial", 12), bg="white",
        ).pack(anchor=tk.W)

        # Suggestions
        suggestions_frame = tk.LabelFrame(bottom, text="Suggested Words", bg="white")
        suggestions_frame.pack(fill=tk.X, pady=5)

        self.suggestions_text = tk.Text(
            suggestions_frame, height=4, font=("Courier", 14, "bold"),
            bg="#f8f9fa", state=tk.DISABLED, wrap=tk.WORD,
        )
        self.suggestions_text.pack(fill=tk.X, padx=5, pady=5)

        # Reset button
        tk.Button(
            bottom, text="Reset Game", command=self._reset_game,
        ).pack(pady=5)

    def _cycle_letter_color(self, position: int) -> None:
        current = self.button_colors[position]
        btn = self.letter_buttons[position]

        if current == 'default':
            self.button_colors[position] = 'green'
            btn.configure(bg=GREEN_COLOR, fg=TEXT_COLOR)
        elif current == 'green':
            self.button_colors[position] = 'yellow'
            btn.configure(bg=YELLOW_COLOR, fg=TEXT_COLOR)
        elif current == 'yellow':
            self.button_colors[position] = 'gray'
            btn.configure(bg=GRAY_COLOR, fg=TEXT_COLOR)
        else:
            self.button_colors[position] = 'default'
            btn.configure(bg=DEFAULT_COLOR, fg=BLACK)

    def _process_guess(self) -> None:
        guess = self.word_input.get().strip().upper()

        if len(guess) != WORD_LENGTH:
            messagebox.showerror("Input Error", "Please enter exactly 5 letters.")
            return
        if not guess.isalpha():
            messagebox.showerror("Input Error", "Please enter only letters.")
            return

        # Update button labels
        for i in range(WORD_LENGTH):
            self.letter_buttons[i].configure(text=guess[i])

        # Check all colors are set
        if any(c == 'default' for c in self.button_colors):
            messagebox.showerror("Input Error", "Please set the color for all letters by clicking on them.")
            return

        feedback = self._get_feedback_from_buttons()
        self.current_guess += 1

        self.already_guessed.append(guess)
        self._update_constraints(guess, feedback)
        self._filter_possible_words()
        self._add_to_history(guess, feedback)
        self._update_suggestions()
        self._reset_input_panel()
        self._update_status()

    def _get_feedback_from_buttons(self) -> str:
        mapping = {'green': GREEN, 'yellow': YELLOW, 'gray': GRAY}
        return "".join(mapping[c] for c in self.button_colors)

    def _add_to_history(self, guess: str, feedback: str) -> None:
        row = tk.Frame(self.history_inner, bg="white")
        row.pack(anchor=tk.W, pady=2)

        tk.Label(
            row, text=f"Guess {self.current_guess}: ",
            font=("Arial", 12, "bold"), bg="white",
        ).pack(side=tk.LEFT)

        color_map = {GREEN: GREEN_COLOR, YELLOW: YELLOW_COLOR, GRAY: GRAY_COLOR}
        for i in range(WORD_LENGTH):
            lbl = tk.Label(
                row, text=guess[i], width=2, font=("Arial", 12, "bold"),
                bg=color_map[feedback[i]], fg=TEXT_COLOR,
                relief="solid", borderwidth=1,
            )
            lbl.pack(side=tk.LEFT, padx=1)

        # Scroll to bottom
        self.history_canvas.update_idletasks()
        self.history_canvas.yview_moveto(1.0)

    def _reset_input_panel(self) -> None:
        self.word_input.delete(0, tk.END)
        self.button_colors = ['default'] * WORD_LENGTH
        for btn in self.letter_buttons:
            btn.configure(text="-", bg=DEFAULT_COLOR, fg=BLACK)

    def _update_status(self) -> None:
        remaining = len(self.possible_words)
        if remaining == 0:
            self.status_var.set("No possible words found. Check your input for errors.")
        elif remaining == 1:
            self.status_var.set(f"Found the answer: {next(iter(self.possible_words))}")
        else:
            self.status_var.set(
                f"Guess {self.current_guess}/6 complete. {remaining} possible words remaining."
            )

    def _reset_game(self) -> None:
        self.possible_words = self._load_words()
        self.letters_in_word.clear()
        self.letters_not_in_word.clear()
        self.constraint_list.clear()
        self.already_guessed.clear()
        self.current_guess = 0

        self._reset_input_panel()
        for widget in self.history_inner.winfo_children():
            widget.destroy()

        self._update_suggestions()
        self.status_var.set("Game reset! Enter your first guess.")

    # --- Constraint Logic ---

    def _update_constraints(self, guess: str, feedback: str) -> None:
        for i in range(WORD_LENGTH):
            letter = guess[i]
            color = feedback[i]
            self.constraint_list.append(Constraint(letter, i, color))

            if color in (GREEN, YELLOW):
                self.letters_in_word.add(letter)
            elif color == GRAY:
                if letter not in self.letters_in_word:
                    self.letters_not_in_word.add(letter)

        # Clean up: if a letter is confirmed in word, remove from not-in-word
        self.letters_not_in_word -= self.letters_in_word

    def _filter_possible_words(self) -> None:
        self.possible_words = {w for w in self.possible_words if self._is_word_possible(w)}

    def _is_word_possible(self, word: str) -> bool:
        if word in self.already_guessed:
            return False
        for letter in self.letters_not_in_word:
            if letter in word:
                return False
        for letter in self.letters_in_word:
            if letter not in word:
                return False
        for c in self.constraint_list:
            wc = word[c.position]
            if c.colour == GREEN and wc != c.letter:
                return False
            if c.colour == YELLOW and wc == c.letter:
                return False
        return True

    # --- Scoring & Suggestions ---

    def _update_suggestions(self) -> None:
        score_map = self._get_word_score_map(self.possible_words)
        top_entries = sorted(score_map.items(), key=lambda x: x[1], reverse=True)[:10]

        self.suggestions_text.configure(state=tk.NORMAL)
        self.suggestions_text.delete("1.0", tk.END)

        if not top_entries:
            self.suggestions_text.insert(tk.END, "No suggestions available.")
        else:
            line1 = f"Top suggestions ({len(top_entries)}/{len(self.possible_words)}):\n"
            words_top5 = "  ".join(w for w, _ in top_entries[:5])
            self.suggestions_text.insert(tk.END, line1 + words_top5)

            if len(top_entries) > 5:
                words_rest = "  ".join(w for w, _ in top_entries[5:])
                self.suggestions_text.insert(tk.END, f"\n\nOther good options:\n{words_rest}")

        self.suggestions_text.configure(state=tk.DISABLED)

    def _get_word_score_map(self, words: set[str]) -> dict[str, float]:
        if not words:
            return {}

        letter_freq: dict[str, int] = Counter()
        for word in words:
            for c in word:
                letter_freq[c] += 1

        n = len(words)
        letter_score = {ch: count / n for ch, count in letter_freq.items()}

        scores: dict[str, float] = {}
        for word in words:
            unique = set(word)
            score = sum(letter_score.get(c, 0.0) for c in unique)
            score -= self._check_word_for_duplicates(word) * 0.75
            scores[word] = score
        return scores

    @staticmethod
    def _check_word_for_duplicates(word: str) -> int:
        freq = Counter(word)
        pairs = sum(1 for v in freq.values() if v == 2)
        triples = sum(1 for v in freq.values() if v == 3)

        if pairs == 1 and triples == 1:
            return 4
        if pairs == 2:
            return 3
        if triples == 1:
            return 2
        if pairs == 1:
            return 1
        return 0

    # --- Dictionary Loading ---

    def _load_words(self) -> set[str]:
        words: set[str] = set()
        dict_file = "words.txt"

        paths_to_try = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        paths_to_try.append(os.path.join(script_dir, dict_file))
        paths_to_try.append(dict_file)
        paths_to_try.append(os.path.join(script_dir, "src", "main", "resources", dict_file))

        for path in paths_to_try:
            if os.path.isfile(path):
                try:
                    with open(path, "r") as f:
                        for line in f:
                            word = line.strip().upper()
                            if len(word) == WORD_LENGTH and word.isalpha():
                                words.add(word)
                    if words:
                        return words
                except IOError as e:
                    print(f"Error reading dictionary file: {e}", file=sys.stderr)

        # Fallback sample words
        print("Warning: Could not find words.txt, using sample words.", file=sys.stderr)
        fallback = [
            "ABOUT", "ABOVE", "AFTER", "AGAIN", "APPLE",
            "BAKER", "BEACH", "BREAD", "CHAIR", "CHAIN",
        ]
        return set(fallback)

    def run(self) -> None:
        self.root.mainloop()


def main():
    app = WordleHelperGUI()
    app.run()


if __name__ == "__main__":
    main()
