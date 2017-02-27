import random
import re
import os


DICTIONARY = '/usr/share/dict/words'
# default file is system dictionary


def print_intro():
    os.system('clear')
    print("\nWelcome to the Mystery Word Game!\n")
    print("I will pick a word, and you will guess letters in that word. ")
    print("If you guess the complete word, you win. ")
    print("If you guess a wrong letter too many times, you lose. \n")
    print("Let's play! \n\n")


def get_difficulty():
    level = input("Do you want an easy, medium, or hard game? "
                  "(easy/medium/hard) ")
    if (level.lower() == "easy" or
       level.lower() == "medium" or
       level.lower() == "hard"):
        return level
    else:
        print("I do not understand.  Please try again. ")
        return get_difficulty()


def get_source():
    source = input("\nWhich source would you like your word to come from? "
                   "\n1) A dictionary (default)"
                   "\n2) A second grade reading level word list "
                   "\nPlease press 1 or 2. ")
    if source == '1' or source == '2':
        return source
    else:
        print("I do not understand.  Pleasee try again. ")
        return get_source()


def get_word_list(difficulty, file=DICTIONARY):
    # default file is system dictionary, but can provide arg to change
    # just pass it (difficulty, file="sample.txt") for any file in this folder
    # or an absolute path to any other source material
    # Careful--a file without words in the specified ranges could lead to
    # errors by creating an empty word_list that is indexed out of bounds later
    # Could try adding user interaction for cases like this in the future
    word_list = []
    start_range = 0
    end_range = 0

    if difficulty == "easy":
        start_range = 4
        end_range = 6
    elif difficulty == "medium":
        start_range = 6
        end_range = 8
    else:
        start_range = 8

    if difficulty == "easy" or difficulty == "medium":
        with open(file, 'r') as f:
            for line in f: # is strip() necessary?
                line_list = [clean_sentence(word.strip())
                             for word in line.split()
                             if len(clean_sentence(word.strip())) >= start_range
                             and len(clean_sentence(word.strip())) <= end_range]
                word_list += line_list
    else:
        with open(file, 'r') as f:
            for line in f:
                for word in line.split():
                    if len(clean_sentence(word.strip())) >= start_range:
                        word_list.append(clean_sentence(word.strip()))
#    word_list = list(set(word_list))
#    Converting to a set and back to remove duplicates probably improves
#    efficiency later with smaller base to search but at the moment
#    introduces a randomness to the order I don't know how to deal with
#    in the unittest we're supposed to do so commented it out
    return word_list


def clean_sentence(sentence):
    return re.sub(r'[^A-Za-z]', '', sentence.lower())
    # how would this function change if using another language dictionary?
    # i.e. deal with accent marks, or can this only handle English?
    # what about contractions?
    # how would this change to allow hyphenated words?
    # how would the rest of the game have to change to accept hyphens?


def get_word(word_list):
    return word_list[(random.randint(0, (len(word_list)-1)))]


def get_tries():
    # In case you want to change the number of tries via either user input
    # or added difficulty settings later where you pass an arg for it
    tries = 8
    return tries


def print_hints(word):
    print("\nMy word has {} letters. \n".format(len(word)))
    # might flesh out more later with other useful info about your word
    # could ask user if they want a hint
    # could pass incorrect_guesses and tell another letter not in word
    # could ask for number of hints and give a random one from many


def display_word(word, correct_guesses):
    print("  ", end=" ")
    for i in word:
        if i in correct_guesses:
            print(i, end=" ")
        else:
            print("_", end=" ")
    print("  ", end=" ")


def get_guess():
    guess = input("Guess a letter: ")
    guess = clean_sentence(guess)
    if len(guess) == 1:
        return guess
    else:
        print("That is not a letter. ")
        return get_guess()


def is_repeat(guess, correct, wrong, tries):
    # check order of operations for in/and/or/not to see when paren are needed
    if ((guess in correct) or (guess in wrong)):
        print("\nYou've already guessed the letter {}. ".format(guess))
        print("You still have {} tries left. \n".format(tries-len(wrong)))
        return True
    else:
        return False


def is_win(word, correct_guesses):
    word_core = ""
    word_core = "".join(set(word)) # do I have to join back to string?
    if len(word_core) == len(correct_guesses):
        return True
    else:
        return False

def play_round(my_word):
    # keep debating whether I want this in main or not to keep main simple
    my_guess = ""
    my_win = False
    my_tries = 0
    wrong_guesses = []
    correct_guesses = []

    my_tries = get_tries()

    while len(wrong_guesses) < my_tries and not my_win:
        display_word(my_word, correct_guesses) # should there be a clear scrn?
        my_guess = get_guess()

        while (is_repeat(my_guess, correct_guesses, wrong_guesses, my_tries)):
            display_word(my_word, correct_guesses)
            my_guess = get_guess()

        if my_guess in my_word:
            correct_guesses.append(my_guess)
        else:
            wrong_guesses.append(my_guess)

        my_win = is_win(my_word, correct_guesses)

    return my_win


def print_final(win, word):
    if win:
        print("\nYou win! ")
    else:
        print("\nSorry, you ran out of tries.  You lose. ")
    print("The word was {}. \n".format(word))


def new_game():
    again = input("Would you like to play again? (y/n) ")
    again = again.lower()
    if again == "y":
        main()
    elif again == "n":
        os.system('clear')
        return
    else:
        print("I do not understand.  Please try again. ")
        return new_game()


def main():
    my_level = ""
    my_source = ""
    my_word_list = []
    my_word = ""
    my_win = False

    print_intro()

    my_level = get_difficulty()
    my_source = get_source()
    if my_source == '1':
        my_word_list = get_word_list(my_level)
    else:
        my_word_list = get_word_list(my_level, file="second_grade_words.txt")
    # change the above args to (my_level, file="sample.txt") in this folder
    # or provide an absolute path for other source files than the dictionary
    # This is great if you'd like to provide a source at an easier reading level
    my_word = get_word(my_word_list)

    print_hints(my_word)

    my_win = play_round(my_word) # either define my_win here or move this below

    print_final(my_win, my_word)
    # Although really, I guess this whole thing could be written as:
    # my_word = get_word(get_word_list(get_difficulty()))
    # print_final(play_round(my_word), my_word)
    # I find the current spread out form more readable.

    new_game()


if __name__ == '__main__':
    main()
