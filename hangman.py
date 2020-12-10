# Problem Set 2, hangman.py
# Name: Ivan Naezhii 
# Collaborators: - 
# Time spent: 

# Hangman Game
# -----------------------------------
import random
import string

WORDLIST_FILENAME = "words.txt"
INITIAL_GUESSES = 6
INITIAL_WARNINGS = 3
VOWELS = {'a', 'e', 'i', 'o', 'u'}
VACANT_PLACE = '_'

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
    lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
    assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
    False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
    which letters in secret_word have been guessed so far.
    '''
    guessed_word = list(secret_word)
    for i in range(len(secret_word)):
        if secret_word[i] not in letters_guessed:
            guessed_word[i] = VACANT_PLACE + ' '
    guessed_word = ''.join(guessed_word)
    return guessed_word.strip()


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
    yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    available_letters = []
    for letter in alphabet:
        if letter not in letters_guessed:
            available_letters.append(letter)
    return ''.join(available_letters)


def start_message_define(secret_word, warnings):
    print(f"""Welcome to the game Hangman!
I am thinking of a word that is {len(secret_word)} letters long.
You have {warnings} warnings left.""")


def try_message_define(guesses, letters_guessed):
    print(f"""-------------
You have {guesses} guesses left.
Available letters: {get_available_letters(letters_guessed)}""")


def warnings_update(warnings, guesses):
    '''
    if the user inputs anything besides an alphabet or a letter that has already been guessed
    '''
    if warnings == 0:
        return warnings, guesses - 1
    return warnings - 1, guesses


def warning_check(new_letter, letters_guessed, warnings, current_guess_state):
    '''
    new_letter: entered letter in lower case
    letters_guessed: list (of letters), which letters have been guessed so far
    warnings: number of warnings at the moment
    current_guess_state: string, comprised of letters, underscores (_), and spaces that represents
    which letters in secret_word have been guessed so far.
    returns: warning message and boolean, True if we have warning.
    '''
    msg = f'You have {warnings-1} warnings left:'
    if warnings == 0:
        msg = 'You have no warnings left so you lose one guess:'
    if len(new_letter) != 1:
        return f'Oops! It must be 1 letter. {msg} {current_guess_state}', True
    if not new_letter.isalpha():
        return f'Oops! That is not a valid letter. {msg} {current_guess_state}', True
    if new_letter in letters_guessed:
        return f"Oops! You've already guessed that letter. {msg} {current_guess_state}", True
    return '', False

def guess_check(new_letter, secret_word, guesses, current_guess_state):
    '''
    new_letter: entered letter in lower case
    secret_word: string, the secret word to guess.
    guesses: number of guesses at the moment
    current_guess_state: string, comprised of letters, underscores (_), and spaces that represents
    which letters in secret_word have been guessed so far.
    returns: guess message and new number of guesses
    '''
    if new_letter not in set(secret_word):
        if new_letter in VOWELS:
            return f'Oops! That letter is not in my word: {current_guess_state}', guesses - 2
        return f'Oops! That letter is not in my word: {current_guess_state}', guesses - 1
    return f'Good guess: {current_guess_state}', guesses


def get_score(secret_word, guesses):
    '''
    secret_word: string, the secret word to guess.
    returns: the score
    '''
    unique_letters = set(secret_word)
    return len(unique_letters) * guesses


def ending_message_define(secret_word, guesses):
    print('-' * 13) 
    if guesses <= 0:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
    else:
        print(f'Congratulations, you won! Your total score for this game is: {get_score(secret_word, guesses)}')


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
            corresponding letters of other_word, or the letter is the special symbol
            _ , and my_word and other_word are of the same length;
            False otherwise: 
    '''

    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] != '_' and  (my_word[i] != other_word[i] or 
            my_word.count(my_word[i]) != other_word.count(my_word[i])):
            return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
                        Keep in mind that in hangman when a letter is guessed, all the positions
                        at which that letter occurs in the secret word are revealed.
                        Therefore, the hidden letter(_ ) cannot be one of the letters in the word
                        that has already been revealed.

    '''
    #create list for possible_words
    possible_words = [] 
    my_word_replaced = my_word.replace(VACANT_PLACE + ' ', '_') 
    
    #add word to our list
    for word in wordlist:
        if match_with_gaps(my_word_replaced, word):
            possible_words.append(word) 

    #print our list
    if len(possible_words) != 0:
        print('Possible word matches are:', ', '.join(possible_words)) 
    else:
        print('No matches found')


def hangman(secret_word, hints=False):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
    letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses
    * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
    sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computer's word.
    * After each guess, you should display to the user the 
    partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    guesses = INITIAL_GUESSES
    warnings = INITIAL_WARNINGS
    letters_guessed = set()
    current_guess_state = get_guessed_word(secret_word, letters_guessed)
    
    start_message_define(secret_word, warnings)

    while (not is_word_guessed(secret_word, letters_guessed)) and guesses > 0:
        try_message_define(guesses, letters_guessed)
        new_letter = input('Please guess a letter: ').lower()
        #hints check
        if hints and new_letter == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        #warning check
        msg, check_result = warning_check(new_letter, letters_guessed, warnings, current_guess_state)
        if check_result:
            warnings, guesses = warnings_update(warnings, guesses)
            print(msg)
        else:
            letters_guessed.add(new_letter)
            #is new_letter good or bad guess?
            current_guess_state = get_guessed_word(secret_word, letters_guessed)
            guess_result, guesses = guess_check(new_letter, secret_word, guesses, current_guess_state)
            print(guess_result)
            
    #game ending message    
    print(ending_message_define(secret_word, guesses))


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
        letters the secret_word contains and how many guesses s/he starts with.
        
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
        s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
        
    * The user should receive feedback immediately after each guess 
        about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
        partially guessed word so far.
        
    * If the guess is the symbol *, print out all words in wordlist that
        matches the current guessed word. 

    Follows the other limitations detailed in the problem write-up.
    '''
    hangman(secret_word, True)


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
