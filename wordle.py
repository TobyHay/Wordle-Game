import random
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-w", "--word", type=str)
args = parser.parse_args()


def intro_message() -> None:
    print('''\nWelcome to Wordle! Your goal is to guess the 5-letter word.

Insert "Q" any time to quit the game.
Insert "1" to receive a list of all possible words left.\n''')


def import_words() -> tuple[list, list]:
    url_1 = 'https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/d9cddf5e16140df9e14f19c2de76a0ef36fd2748/wordle-La.txt'
    url_2 = 'https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/d9cddf5e16140df9e14f19c2de76a0ef36fd2748/wordle-Ta.txt'

    response_1 = requests.get(url_1, timeout=10)
    response_2 = requests.get(url_2, timeout=10)

    soup_1 = BeautifulSoup(response_1.text, 'html.parser')
    soup_2 = BeautifulSoup(response_2.text, 'html.parser')

    words_1 = soup_1.get_text()
    words_2 = soup_2.get_text()

    answer_list = words_1.split("\n")
    word_list = words_1.split("\n") + words_2.split("\n")

    return (answer_list, word_list)


def output(guesses: list[str], results: list[str], attempt: int, keyboard: list[str]) -> None:
    for n in range(attempt):
        print("    {} <- {}\n".format(" ".join(results[n-1]), guesses[n]))

    for n in range(attempt, 6):
        print("    {}\n".format(" ".join(results[n-1])))

    print(" ".join(keyboard))


def user_input(attempt: int) -> str:
    print(("Guess {}/6: ".format(attempt+1)).lower())
    if attempt == 0 and args.word:
        return args.word

    value = input(f"Guess {attempt+1}/6: ").lower().strip()
    return value


def valid_input(value: str, alphabet: list[str]) -> bool:
    if len(value) != 5:
        print('Guess must be 5 letters long')
        return False

    elif not value in word_list:
        print('Guess is not in word list ')
        return False

    for letter in value:
        if not letter in alphabet:
            print('Guess must only contain letters')
            return False
        print()
        return True


def letter_result(current_guess, guesses, results, n, keyboard) -> None:
    guesses.append(current_guess.upper())

    letters_left = remove_correct_letters(current_guess, wordle)
    for i, letter in enumerate(current_guess):
        # Correct Spot
        if letter == wordle[i]:
            results[n-1][i] = ('{}'.format(letter.upper()))

        # Wrong Spot
        elif letter in letters_left:
            results[n-1][i] = ('{}'.format(letter.lower()))
            letters_left.remove(letter)

        else:  # No Spot
            if letter.upper() in keyboard:
                letter_index = keyboard.index(letter.upper())
                keyboard[letter_index] = ' '


def remove_correct_letters(current_guess, wordle) -> list:
    letters_left = wordle[::]
    for i, letter in enumerate(current_guess):
        if letter == wordle[i]:
            letters_left.remove(letter)
    return letters_left


def win_game(wordle: list[str], guess: str) -> bool:
    if guess and list(guess) == wordle:
        print('Well done, you win!')
        return True


def lose_game(attempt: int, wordle: list[str]) -> bool:
    if attempt > 5:
        print('You lost! The word was {}'.format("".join(wordle).upper()))
        return True


# ---------------------- Incomplete  ----------------------
def get_letter_info(guesses: list[str], wordle: list[str], alphabet: list[str]) -> dict:

    correct_word = [0, 0, 0, 0, 0]
    wrong_letters = {letter: [] for letter in alphabet}

    for guess in guesses:
        for i, letter in enumerate(guess.lower()):
            # No Spot
            if letter not in wordle:
                wrong_letters[letter] = [0, 1, 2, 3, 4]

            # Wrong Spot
            elif letter != wordle[i]:
                wrong_letters[letter].append(i)
                correct_word.append(letter)

            # Correct Spot
            elif letter == wordle[i]:
                correct_word[i] = letter
    return correct_word, wrong_letters


def show_words_left(answer_list, info) -> None:
    correct_word, wrong_letters = info
    answers = answer_list[::]

    for word in answer_list:

        # Remove word if it doesn't include known correct letter
        for letter in correct_word:
            if letter and letter not in word:
                answers.remove(word) if word in answers else None

        for i, letter in enumerate(word):

            # Remove word if letter is in a defined correct spot
            if correct_word[i] and letter != correct_word[i]:
                answers.remove(word) if word in answers else None

            # Remove word if letter is in a defined wrong spot
            elif i in wrong_letters.get(letter):
                answers.remove(word) if word in answers else None

    column_output = ""
    for i in range(0, len(answers)//4):
        i *= 4
        column_output += answers[i] + "  " + answers[i+1] + \
            "  " + answers[i+2] + "  " + answers[i+3] + "\n"
    remainder = len(answers) % 4
    if remainder:
        last_row = "  ".join(answers[-remainder:])
        column_output += last_row

    print(f"{"\n"*20}")
    print(f"Possible answers: {len(answers)}")
    print(column_output)
    # ---------------------- Incomplete  ----------------------


def guess():
    alphabet = list('abcdefghijklmnopqrstuvwxyz')

    correct_word = [0, 0, 0, 0, 0]
    wrong_letters = {letter: [] for letter in alphabet}

    print("Enter green letters in order, with 0 for unknown.")
    incorrect_input = True
    while incorrect_input:
        green = input("Green: ").lower()
        if green == "q":
            return

        if not green:
            incorrect_input = False
        if len(green) == 5:
            incorrect_input = False

    print("Enter yellow letters with the position number after.\ne.g. a0 b1 c2 ...")
    yellow = input("Yellow: ").lower()
    if yellow == "q":
        return

    yellows = yellow.split(" ")

    incorrect_input = True
    while incorrect_input:
        print("Enter all wrong letters")
        grey = input("Wrong: ").lower()
        if grey == "q":
            return

        incorrect_input = False
        for letter in grey:
            if letter not in alphabet:
                incorrect_input = True

    # Green
    if green:
        for i, letter in enumerate(green):
            if letter != "0":
                correct_word[i] = letter

    # Yellow
    if yellow:
        for letter in yellows:
            i = int(letter[1])

            print(wrong_letters)
            wrong_letters[letter[0]].append(i)
            correct_word.append(letter[0])

    # Grey
    if grey:
        for letter in grey:
            wrong_letters[letter] = [0, 1, 2, 3, 4]

    # ---- Debugging ----
    # print()
    # print(correct_word)
    # print()
    # print(wrong_letters)

    info = correct_word, wrong_letters
    show_words_left(answer_list, info)


# ---------------------- Main Game Code ---------------------


def play() -> None:

    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    keyboard = list('QWERTYUIOP\nASDFGHJKL\n ZXCVBNM\n')

    guesses = []
    results = [['_']*5, ['_']*5, ['_']*5, ['_']*5, ['_']*5, ['_']*5,]

    intro_message()
    # input("Press enter to start:\n")

    attempt = 0
    current_guess = ""
    while True:
        output(guesses, results, attempt, keyboard)

        if win_game(wordle, current_guess):
            break

        if lose_game(attempt, wordle):
            break

        current_guess = user_input(attempt)

        if current_guess.upper() == "Q":
            print('Task quit successfully')
            break

        if current_guess == "1":
            info = get_letter_info(guesses, wordle, alphabet)
            show_words_left(answer_list, info)

            if input("Press enter to continue playing:").upper() == "Q":
                print('Task quit successfully')
                break
            print()
            continue

        if not valid_input(current_guess, alphabet):
            continue

        letter_result(current_guess, guesses, results, attempt, keyboard)

        attempt += 1


# ------------------- Start Game -------------------
answer_list, word_list = import_words()
wordle_num = random.randint(0, len(answer_list))

wordle = list(answer_list[wordle_num])

# GIVE CUSSTOM ANSWER
custom_answer = ""
if custom_answer:
    wordle = list(custom_answer)

if __name__ == "__main__":
    play()
    # guess()
