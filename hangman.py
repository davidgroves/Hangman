#!/usr/bin/env python3

import random
import string
import sys
import argparse

def show_word(word, already_guessed):
    '''

    :param word: The word the person is trying to guess.
    :param already_guessed: A list of the letters they have already attempted to guess.
    :return: The word to print, with letters gussed printed, and *'s for the unprinted letters.
    '''
    output = ""
    for i in word:
        if i in already_guessed:
            output += i
        else:
            output += "*"
    return output


def get_input(already_guessed, lives):
    '''

    :param already_guessed: The words the person has already guessed, so they can't try things twice.
    :param lives: How many lives they have so we can print this.
    :return: The letter they guessed, always in lower case.
    '''
    while True:
        try:
            letter = input("Enter a letter to guess. (You have {} lives remaining): ".format(lives))
            if len(letter) != 1:
                raise ValueError("You put in nothing, or more than one letter !")
                break
            if letter.lower() not in string.ascii_lowercase:
                raise ValueError("You didn't enter a letter !")
                break
            if letter in already_guessed:
                raise ValueError("You already tried that letter. Pick something new !")
                break
        except ValueError as e:
            print(e)
        else:
            return letter.lower()


def check_win(word, already_guessed):
    '''

    :param word: The word to be guessed.
    :param already_guessed: The letters already guessed.
    :return: True if the won, False otherwise.
    '''
    return not set(word).difference(already_guessed)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lives", help="The number of lives", default="6", type=int)
    args = parser.parse_args()
    lives = args.lives

    # Load our wordlist from our file.
    with open("wordlist.txt") as f:
        wordlist = f.readlines()

    # Get the random word we will have the person guess. Striping the newline character.
    word = random.choice(wordlist).strip()

    # Setup a list of what has already been attempted.
    already_guessed = []

    # Main game loop
    while lives > 0:
        print(show_word(word=word, already_guessed=already_guessed))
        letter = get_input(already_guessed=already_guessed, lives=lives)

        if letter not in word:
            # You guessed incorrectly.
            lives -= 1

        # Note you guessed correctly
        already_guessed.append(letter)

        # Check if you have won.
        if check_win(word=word, already_guessed=already_guessed):
            print("Well done, you have won !")
            print("The word was {}, and you had {} lives remaining !".format(word, lives))
            sys.exit(0)

    # We only get here if you have lost.

    print("Sorry, but you are out of lives. The word was {}".format(word))
    sys.exit(1)
