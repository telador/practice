# Problem Set 2, hangman.py
# Name: Ivan Naezhii 
# Collaborators: - 
# Time spent: 

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
WORDLIST_FILENAME = "words.txt"


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
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

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
    checker = True
    for t in secret_word:
      if letters_guessed.count(t)==0:
        checker = False
        break
    return checker



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for t in secret_word:
      if letters_guessed.count(t)==0:
        guessed_word += '_ '
      else:
        guessed_word += t
    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    for t in letters_guessed:
      alphabet = alphabet.replace(t,'') 
    return alphabet
    

def print_line():
    print('-------------')


def word_score(secret_word):
    st = set()
    for t in secret_word:
      st.add(t)
    return len(st)


def hangman(secret_word):
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
    guesses = 6
    warnings = 3
    letters_guessed = []
    vowels = ['a','e','i','o','u']
    print('I am thinking of a word that is '+str(len(secret_word))+' letters long.')
    print('You have '+str(warnings)+' warnings left.')
    while True:
      print_line()
      if guesses <= 0:
        print('Sorry, you ran out of guesses. The word was '+secret_word)
        break
      print('You have '+str(guesses)+' guesses left.')
      print('Available letters: '+get_available_letters(letters_guessed))
      new_letter = input('Please guess a letter: ')
      new_letter = new_letter.lower()
      if new_letter.isalpha()==False:
        if warnings>0:
          warnings -= 1
        else:
          guesses -= 1
        print('Oops! That is not a valid letter. You have '+str(warnings)+' warnings left: '+get_guessed_word(secret_word,letters_guessed))
      elif letters_guessed.count(new_letter)>0:
        if warnings>0:
          warnings -= 1
        else:
          guesses -= 1
        print("Oops! You've already guessed that letter. You have "+str(warnings)+' warnings left: '+get_guessed_word(secret_word,letters_guessed))
      else:
        letters_guessed.append(new_letter)  
        if secret_word.count(new_letter)==0:
          guesses -= 1
          if vowels.count(new_letter)>0:
            guesses -= 1
          print('Oops! That letter is not in my word: ',get_guessed_word(secret_word,letters_guessed))
        else:
          print('Good guess: ',get_guessed_word(secret_word,letters_guessed))
          if is_word_guessed(secret_word,letters_guessed):
            print_line()
            print('Congratulations, you won! Your total score for this game is: '+str(guesses*word_score(secret_word)))
            break
        

  



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    checker = True
    if len(my_word)!=len(other_word):
      checker = False
    else:
      for i in range(len(my_word)):
        if my_word[i]=='_':
          pass
        elif my_word[i]==other_word[i] and my_word.count(my_word[i])==other_word.count(my_word[i]):
          pass
        else:
          checker = False
    return checker


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    flag = True
    my_word_replaced = my_word.replace('_ ','_')
    for i in range(len(wordlist)):
      if match_with_gaps(my_word_replaced,wordlist[i]):
        if flag:
          print('Possible word matches are: ',end='')
          flag = False
        print(wordlist[i],end=' ')
    if flag:
      print('No matches found',end='')
    print('')


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
    guesses = 6
    warnings = 3
    letters_guessed = []
    vowels = ['a','e','i','o','u']
    print('I am thinking of a word that is '+str(len(secret_word))+' letters long.')
    print('You have '+str(warnings)+' warnings left.')
    while True:
      print_line()
      if guesses <= 0:
        print('Sorry, you ran out of guesses. The word was '+secret_word)
        break
      print('You have '+str(guesses)+' guesses left.')
      print('Available letters: '+get_available_letters(letters_guessed))
      new_letter = input('Please guess a letter: ')
      if new_letter == '*':
        show_possible_matches(get_guessed_word(secret_word,letters_guessed))
        continue
      new_letter = new_letter.lower()
      if new_letter.isalpha()==False:
        if warnings>0:
          warnings -= 1
        else:
          guesses -= 1
        print('Oops! That is not a valid letter. You have '+str(warnings)+' warnings left: '+get_guessed_word(secret_word,letters_guessed))
      elif letters_guessed.count(new_letter)>0:
        if warnings>0:
          warnings -= 1
        else:
          guesses -= 1
        print("Oops! You've already guessed that letter. You have "+str(warnings)+' warnings left: '+get_guessed_word(secret_word,letters_guessed))
      else:
        letters_guessed.append(new_letter)  
        if secret_word.count(new_letter)==0:
          guesses -= 1
          if vowels.count(new_letter)>0:
            guesses -= 1
          print('Oops! That letter is not in my word: ',get_guessed_word(secret_word,letters_guessed))
        else:
          print('Good guess: ',get_guessed_word(secret_word,letters_guessed))
          if is_word_guessed(secret_word,letters_guessed):
            print_line()
            print('Congratulations, you won! Your total score for this game is: '+str(guesses*word_score(secret_word)))
            break



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    #s = input()
    #hangman(s)

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
