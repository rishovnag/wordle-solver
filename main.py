"""
WordleSolver - Main entry point.
Provides a menu to launch the Wordle Game, CLI Helper, or GUI Helper.
"""

import sys


def main():
    print("=" * 45)
    print("  Welcome to WordleSolver (Python Edition)")
    print("=" * 45)
    print()
    print("Choose a mode:")
    print("  1. Wordle Game       (play Wordle with a GUI)")
    print("  2. Wordle Helper CLI (get suggestions via terminal)")
    print("  3. Wordle Helper GUI (get suggestions via GUI)")
    print()

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        from wordle_game import main as game_main
        game_main()
    elif choice == "2":
        from wordle_helper import main as helper_main
        helper_main()
    elif choice == "3":
        from wordle_helper_gui import main as helper_gui_main
        helper_gui_main()
    else:
        print(f"Invalid choice: '{choice}'. Please run again and enter 1, 2, or 3.")
        sys.exit(1)


if __name__ == "__main__":
    main()
