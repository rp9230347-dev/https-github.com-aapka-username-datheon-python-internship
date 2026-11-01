"""Task 1 - Terminal Hangman with ASCII art (6 attempts)."""
import random
import os

MAX_MISTAKES = 6

STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]

FALLBACK_WORDS = ["python", "programming", "hangman", "internship", "keyboard", "algorithm"]


def load_words(path="words.txt", min_len=5):
    """Load words from the English word list; fall back to a small built-in list."""
    here = os.path.dirname(os.path.abspath(__file__))
    full = os.path.join(here, path)
    try:
        with open(full, encoding="utf-8") as f:
            words = [w.strip().lower() for w in f if len(w.strip()) >= min_len and w.strip().isalpha()]
        return words or FALLBACK_WORDS
    except OSError:
        return FALLBACK_WORDS


def masked(word, guessed):
    return " ".join(c.upper() if c in guessed else "_" for c in word)


def play(word=None):
    word = word or random.choice(load_words())
    guessed = set()
    mistakes = 0

    print("\n=== HANGMAN ===  (you have 6 wrong attempts)")
    while mistakes < MAX_MISTAKES and set(word) - guessed:
        print(STAGES[mistakes])
        print("\nWord   :", masked(word, guessed))
        print("Guessed:", " ".join(sorted(g.upper() for g in guessed)) or "-")
        print(f"Lives  : {MAX_MISTAKES - mistakes}")

        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        if guess in guessed:
            print(f"You already guessed '{guess.upper()}' - no penalty.")
            continue

        guessed.add(guess)
        if guess in word:
            print("Good guess!")
        else:
            mistakes += 1
            print("Wrong!")

    print(STAGES[mistakes])
    if set(word) <= guessed:
        print(f"\nYou won! The word was '{word.upper()}'.")
    else:
        print(f"\nGame over! The word was '{word.upper()}'.")


def main():
    while True:
        play()
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
