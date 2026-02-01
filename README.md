# Capstone-Project

## Introduction

This project is to show my understanding of python after learning the fundamentals and compiling them together into one piece of work.
This consists of a Wordle clone, which uses the list of all 5 letter words by [scholtes](https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d)

The `wordle.py` file is designed to run in the terminal, with 2 main features in the functions `play()` and `guess()`.

# Play function

A random word from the word list will be selected, you must guess the word within 6 attempts.
Input a 5 letter word and the code will output if any of the letters were located in the correct spot, and will remove all known irrelevant letters from the keys shown.

## Example guess

If the wordle to guess is "WORDS" and the input given by the user is "WIRED"  
The "W" and "R" which are in the correct spot will be shown as uppercase: "W, R"  
The "D" which is in the word but in the wrong spot will be shown as lowercarse: "d"  

Therefore, the output will give:

```
    W _ R _ d <- WIRED

    _ _ _ _ _

    _ _ _ _ _

    _ _ _ _ _

    _ _ _ _ _

    _ _ _ _ _

Q W   R T Y U   O P
 A S D F G H J K L
   Z X C V B N M
```

## Pressing 1 to give the words left

Throughout guessing the word, there is an option to enter `1` into the terminal. This will provide a list of all words from the original word list that fit the restrictions of the information provided from your current guesses.


# Guess function

The other function provided in this `wordle.py` file is the `guess()` function. This was inspired by the previously mentioned "press 1 to receive all possible words" feature, but allows you to input all green, yellow and grey letters provided from an external wordle game. This will then output all potential words included in the wordle list provided by [scholtes](https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d).

Note that this list may be out of date so may not guarantee correct results.
