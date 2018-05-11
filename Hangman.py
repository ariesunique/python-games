#####################
# Hangman.py
#
# Simulates a "Hangman" game
#
#
####################

import random
import json
import click


def build_word_map():
    """
    words = {"fruit": ["apple", "banana", "grapes", "pear", "watermelon"], \
             "places": ["school", "church", "library", "mall", "restaurant", "airport"],
             "colors": ["red", "blue", "yellow", "cerulean", "aqua", "magenta", "green", "orange"]}
    """

    with open("hangman_words.json", "r") as infile:
        data = json.load(infile)

    wordmap = {}
    for item in data:
        category = item["category"]
        words = item["words"]
        wordmap[category] = words

    return wordmap


@click.command()
@click.option("--chances", '-c', default=5, type=click.IntRange(1, 10, clamp=True),
              help="The number of wrong letters you can guess before you lose. Must be between 1 and 10.")
def main(chances):
    """Hangman game. Try to guess a random word chosen by the computer. You can guess CHANCES wrong letters before you
    lose. If you guess the word, you win."""

    # load the data
    words = build_word_map()
    num_games_played = 0
    num_wins = 0

    while True:
        num_games_played += 1
        guessed_letters = []
        turns = chances

        # allow user to choose a category
        while True:
            category = input(f"Choose a category {sorted(list(words.keys()))}: ")
            if category in words.keys():
                break
            else:
                print("Please choose a valid category.")

        # once a word is selected, remove it from the list so that it cannot be used again
        word = random.choice(words[category])
        words[category].remove(word)
        if not words[category]:
            del words[category]

        display = list("-" * len(word))
        print(f"{' '.join(display)} ({len(word)}) \n")

        while turns > 0 and '-' in display:
            guess = input(f"Already guessed letters ({''.join(sorted(guessed_letters)).upper()}). Guess a letter: ")
            if not (guess.isalpha() and len(guess) == 1):
                print("Please enter a single letter.")
                continue

            guess = guess.lower()
            if guess not in guessed_letters:
                guessed_letters.append(guess)
            else:
                print("You already guessed that letter.")
                print(f"{' '.join(display)} ({len(word)}) ")
                continue

            if guess in word:
                for i, letter in enumerate(word):
                    if letter == guess:
                        display[i] = letter
                print(f"{' '.join(display)} ({len(word)}) ")
            else:
                turns -= 1
                print(f"Sorry. No {guess}'s in the hidden word. {turns} chances left.")

        if "".join(display) == word:
            print("\nCongratulations! You guessed the word.")
            num_wins += 1
        else:
            print(f"\nThe word was: {word}.")

        while True:
            response = input("Would you like to play again (Y/N)?")
            if response not in "YNyn":
                print("Response not understood.")
            else:
                break

        if response in "Nn":
            print("\nThank you for playing!")
            print("Here are your stats: ")
            print(f"\tYou played {num_games_played} games. You won {num_wins} and lost {num_games_played-num_wins}." +
                  f"Your winning rate is {100*(num_wins/num_games_played):.2f}%.")
            print("Good bye!")
            break


if __name__ == "__main__":
    main()
