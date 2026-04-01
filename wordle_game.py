"""
WordleGame: A tkinter GUI Wordle game.
Ported from the Java Swing WordleGame.java.
"""

import tkinter as tk
from tkinter import messagebox

from dictionary_manager import DictionaryManager


# --- Color Constants ---
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GRAY = "#787c7e"
DARK_GRAY = "#3a3a3c"
WHITE = "#ffffff"
BACKGROUND = "#121213"
RED = "#dc143c"

ROWS = 6
COLS = 5


class WordleGame:
    def __init__(self):
        self.dictionary = DictionaryManager()
        self.target_word = ""
        self.current_row = 0
        self.current_col = 0
        self.game_over = False

        self.root = tk.Tk()
        self.root.title("Wordle Game")
        self.root.configure(bg=BACKGROUND)
        self.root.resizable(False, False)

        self.grid_labels: list[list[tk.Label]] = []
        self.message_var = tk.StringVar(value="Enter a 5-letter word")
        self.target_var = tk.StringVar()
        self.answer_var = tk.StringVar()

        self._init_ui()
        self._start_new_game()
        self._show_instructions()

    def _init_ui(self) -> None:
        # Title
        title = tk.Label(
            self.root, text="WORDLE", font=("Arial", 36, "bold"),
            fg=WHITE, bg=BACKGROUND, pady=20,
        )
        title.pack()

        # Game grid
        grid_frame = tk.Frame(self.root, bg=BACKGROUND, padx=50, pady=20)
        grid_frame.pack()

        for i in range(ROWS):
            row_labels: list[tk.Label] = []
            for j in range(COLS):
                lbl = tk.Label(
                    grid_frame, text="", font=("Arial", 32, "bold"),
                    width=2, height=1, bg=DARK_GRAY, fg=WHITE,
                    relief="solid", borderwidth=2,
                    highlightbackground=DARK_GRAY, highlightthickness=2,
                )
                lbl.grid(row=i, column=j, padx=3, pady=3)
                row_labels.append(lbl)
            self.grid_labels.append(row_labels)

        # Bottom panel
        bottom_frame = tk.Frame(self.root, bg=BACKGROUND, padx=20, pady=10)
        bottom_frame.pack(fill=tk.X)

        # Message label
        msg_label = tk.Label(
            bottom_frame, textvariable=self.message_var,
            font=("Arial", 16), fg=WHITE, bg=BACKGROUND,
        )
        msg_label.pack(pady=5)
        self._message_label = msg_label

        # Buttons
        btn_frame = tk.Frame(bottom_frame, bg=BACKGROUND)
        btn_frame.pack(pady=5)

        reset_btn = tk.Button(
            btn_frame, text="Reset Game", font=("Arial", 14, "bold"),
            bg="#dc143c", fg=WHITE, width=12,
            command=self._reset_game,
        )
        reset_btn.pack(side=tk.LEFT, padx=5)

        new_btn = tk.Button(
            btn_frame, text="New Game", font=("Arial", 14, "bold"),
            bg="#007bff", fg=WHITE, width=12,
            command=self._start_new_game,
        )
        new_btn.pack(side=tk.LEFT, padx=5)

        # Target label (debug)
        target_lbl = tk.Label(
            bottom_frame, textvariable=self.target_var,
            font=("Arial", 12), fg="#d3d3d3", bg=BACKGROUND,
        )
        target_lbl.pack(pady=2)

        # Answer label (shown on loss)
        answer_lbl = tk.Label(
            bottom_frame, textvariable=self.answer_var,
            font=("Arial", 18, "bold"), fg=RED, bg=BACKGROUND,
        )
        answer_lbl.pack(pady=2)

        # Keyboard bindings
        self.root.bind("<Key>", self._on_key)
        self.root.focus_set()

    def _show_instructions(self) -> None:
        instructions = (
            "HOW TO PLAY WORDLE:\n\n"
            "- Guess the 5-letter word in 6 tries\n"
            "- Each guess must be a valid 5-letter word\n"
            "- After each guess, the tiles change color:\n\n"
            "  GREEN: Letter is correct and in the right position\n"
            "  YELLOW: Letter is in the word but wrong position\n"
            "  GRAY: Letter is not in the word\n\n"
            "- Type your guess and press ENTER\n"
            "- Use BACKSPACE to delete letters\n"
            "- Use RESET GAME to clear current progress\n"
            "- Use NEW GAME to start with a different word\n\n"
            "Good luck!"
        )
        messagebox.showinfo("How to Play", instructions)

    def _start_new_game(self) -> None:
        self.target_word = self.dictionary.get_random_answer()
        self._reset_game_state()
        self.target_var.set(f"Target: {self.target_word}")
        self.message_var.set("Enter a 5-letter word")
        self._message_label.configure(fg=WHITE)
        self.answer_var.set("")

    def _reset_game(self) -> None:
        self._reset_game_state()
        self.message_var.set("Game reset! Enter a 5-letter word")
        self._message_label.configure(fg=WHITE)
        self.answer_var.set("")

    def _reset_game_state(self) -> None:
        self.current_row = 0
        self.current_col = 0
        self.game_over = False

        for i in range(ROWS):
            for j in range(COLS):
                self.grid_labels[i][j].configure(
                    text="", bg=DARK_GRAY,
                    highlightbackground=DARK_GRAY,
                )
        self.root.focus_set()

    def _process_guess(self, guess: str) -> None:
        if len(guess) != 5:
            self.message_var.set("Word must be exactly 5 letters!")
            return

        if not self.dictionary.is_valid_word(guess):
            self.message_var.set("Not a valid word!")
            return

        guess_chars = list(guess)
        target_chars = list(self.target_word)
        colors = [None] * 5
        target_used = [False] * 5
        guess_used = [False] * 5

        # First pass: exact matches (green)
        for i in range(5):
            if guess_chars[i] == target_chars[i]:
                colors[i] = GREEN
                target_used[i] = True
                guess_used[i] = True

        # Second pass: partial matches (yellow) and misses (gray)
        for i in range(5):
            if guess_used[i]:
                continue
            found = False
            for j in range(5):
                if not target_used[j] and guess_chars[i] == target_chars[j]:
                    colors[i] = YELLOW
                    target_used[j] = True
                    found = True
                    break
            if not found:
                colors[i] = GRAY

        # Update grid
        for i in range(5):
            self.grid_labels[self.current_row][i].configure(
                text=guess_chars[i], bg=colors[i],
                highlightbackground=colors[i],
            )

        # Check win
        if guess == self.target_word:
            self.game_over = True
            self.message_var.set(f"Congratulations! You won in {self.current_row + 1} tries!")
            self._message_label.configure(fg=GREEN)
            self.answer_var.set("")
            return

        self.current_row += 1
        self.current_col = 0

        # Check lose
        if self.current_row >= ROWS:
            self.game_over = True
            self.message_var.set("Game Over! Better luck next time!")
            self._message_label.configure(fg=RED)
            self.answer_var.set(f"The correct word was: {self.target_word}")

            messagebox.showinfo(
                "Game Over",
                f"Game Over!\n\nThe correct word was: {self.target_word}\n\n"
                "Click 'New Game' to try again with a different word,\n"
                "or 'Reset Game' to try the same word again.",
            )
            print(f"Game Over! The word was: {self.target_word}")
            return

        self.message_var.set(f"Try again... ({ROWS - self.current_row} tries left)")
        self._message_label.configure(fg=WHITE)

    def _on_key(self, event: tk.Event) -> None:
        if self.game_over:
            return

        if event.keysym == "Return":
            guess = "".join(
                self.grid_labels[self.current_row][i].cget("text")
                for i in range(COLS)
            )
            if len(guess) < COLS or "" in [self.grid_labels[self.current_row][i].cget("text") for i in range(COLS)]:
                self.message_var.set("Complete the word first!")
                return
            self._process_guess(guess)

        elif event.keysym == "BackSpace":
            if self.current_col > 0:
                self.current_col -= 1
                self.grid_labels[self.current_row][self.current_col].configure(
                    text="", bg=DARK_GRAY,
                    highlightbackground=DARK_GRAY,
                )

        elif event.char and event.char.isalpha() and self.current_col < COLS:
            letter = event.char.upper()
            self.grid_labels[self.current_row][self.current_col].configure(
                text=letter, bg=DARK_GRAY,
                highlightbackground=WHITE,
            )
            self.current_col += 1

    def run(self) -> None:
        self.root.mainloop()


def main():
    game = WordleGame()
    game.run()


if __name__ == "__main__":
    main()
