"""
WordleHelper: A CLI program to help you play Wordle.
It takes your 5-letter guess and the color feedback for each letter,
then suggests new words.
"""

import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from typing import Optional


# --- Constants ---
WORD_LENGTH = 5
MAX_GUESSES = 5
GREEN = 'g'
YELLOW = 'y'
GRAY = 'x'


@dataclass(frozen=True)
class Constraint:
    """Holds information about a single letter's constraint."""
    letter: str
    position: int
    colour: str


class WordleHelper:
    """A CLI Wordle helper that suggests words based on feedback."""

    def __init__(self):
        self.possible_words: set[str] = self._load_words()
        self.letters_in_word: set[str] = set()
        self.letters_not_in_word: set[str] = set()
        self.constraint_list: list[Constraint] = []
        self.already_guessed: list[str] = []

    def run(self) -> None:
        """Main application loop that drives the game."""
        self._print_welcome()

        for i in range(1, MAX_GUESSES + 1):
            print(f"\n--- GUESS {i} of {MAX_GUESSES} ---")

            if not self._process_guess_and_feedback():
                break

            if not self.possible_words:
                print("No possible words match the criteria. Something might be wrong with the input.")
                break

            self._suggest_next_words()

            if i < MAX_GUESSES and self._should_exit():
                break

        print("\nGame over. Thanks for playing!")

    def _process_guess_and_feedback(self) -> bool:
        """Handles input for a single guess and its feedback, then updates the word list."""
        guess = input("Enter your 5-letter word guess: ").strip().upper()

        if guess == "EXIT":
            print("Exiting Wordle Helper. Goodbye!")
            return False

        if len(guess) != WORD_LENGTH:
            print("Invalid word length. Please enter a 5-letter word.")
            return self._process_guess_and_feedback()

        print(f"Enter the color feedback (g=green, y=yellow, x=gray).")
        print(f"Example: for the word '{guess}', enter 'gyyxg'")
        feedback = input("Your feedback: ").strip().lower()

        if len(feedback) != WORD_LENGTH:
            print("Invalid feedback length. Please enter 5 characters.")
            return self._process_guess_and_feedback()

        self.already_guessed.append(guess)
        self._update_constraints(guess, feedback)
        self._filter_possible_words()
        return True

    def _update_constraints(self, guess: str, feedback: str) -> None:
        """Updates constraints based on the latest guess and feedback."""
        for i in range(WORD_LENGTH):
            letter = guess[i]
            color = feedback[i]

            self.constraint_list.append(Constraint(letter, i, color))

            if color in (GREEN, YELLOW):
                self.letters_in_word.add(letter)
            elif color == GRAY:
                if letter not in self.letters_in_word:
                    self.letters_not_in_word.add(letter)

    def _filter_possible_words(self) -> None:
        """Filters the set of possible words based on current constraints."""
        self.possible_words = {w for w in self.possible_words if self._is_word_possible(w)}

    def _is_word_possible(self, word: str) -> bool:
        """Checks if a word satisfies all accumulated constraints."""
        if word in self.already_guessed:
            return False

        for letter in self.letters_not_in_word:
            if letter in word:
                return False

        for letter in self.letters_in_word:
            if letter not in word:
                return False

        for constraint in self.constraint_list:
            word_char = word[constraint.position]

            if constraint.colour == GREEN and word_char != constraint.letter:
                return False
            if constraint.colour == YELLOW and word_char == constraint.letter:
                return False

        return True

    def _suggest_next_words(self) -> None:
        """Calculates scores for remaining words and suggests the top 5."""
        score_map = self._get_word_score_map(self.possible_words)

        top_five = sorted(score_map.items(), key=lambda x: x[1], reverse=True)[:5]

        print(f"Top {len(top_five)} suggestions for your next guess:")
        print(" ".join(word for word, _ in top_five))

    def _get_word_score_map(self, words: set[str]) -> dict[str, float]:
        """Calculates a score for each word based on letter frequency and uniqueness."""
        if not words:
            return {}

        letter_freq: dict[str, int] = Counter()
        for word in words:
            for c in word:
                letter_freq[c] += 1

        n = len(words)
        letter_score = {ch: count / n for ch, count in letter_freq.items()}

        word_scores: dict[str, float] = {}
        for word in words:
            unique_letters = set(word)
            score = sum(letter_score.get(c, 0.0) for c in unique_letters)
            score -= self._check_word_for_duplicates(word) * 0.75
            word_scores[word] = score

        return word_scores

    @staticmethod
    def _check_word_for_duplicates(word: str) -> int:
        """Returns a penalty score based on duplicate letters."""
        freq = Counter(word)
        pairs = sum(1 for v in freq.values() if v == 2)
        triples = sum(1 for v in freq.values() if v == 3)

        if pairs == 1 and triples == 1:
            return 4  # e.g., MAMMA
        if pairs == 2:
            return 3  # e.g., LEVEL
        if triples == 1:
            return 2  # e.g., SASSY
        if pairs == 1:
            return 1  # e.g., APPLE
        return 0      # e.g., TRAIN

    @staticmethod
    def _should_exit() -> bool:
        """Asks the user if they wish to continue."""
        response = input("\nPress 'Enter' to continue, or type 'exit' to quit: ").strip()
        return response.lower() == "exit"

    @staticmethod
    def _print_welcome() -> None:
        print("Welcome to the Wordle Helper!")
        print("Let's help you find the secret word.")
        print("You can enter 'exit' at any time to quit.")
        print("-" * 40)

    def _load_words(self) -> set[str]:
        """Loads 5-letter words from the dictionary file."""
        words: set[str] = set()
        dict_file = "words.txt"

        # Try script directory first, then current directory
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

        print(f"Error: Could not find the dictionary file: {dict_file}", file=sys.stderr)
        return words


def main():
    WordleHelper().run()


if __name__ == "__main__":
    main()
