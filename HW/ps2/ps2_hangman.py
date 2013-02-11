# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!
def create_blank_word(x):
    board = []
    for i in range(x):
        board.append("_")
    return board

def check_board(board):
    for i in range(len(board)):
        if board[i] == "_":
            return True
    return False

def find_letter(word,guess):
    index = []
    for i in range(len(word)):
        if word[i] == guess:
            index.append(i)
    return index

def board_replace_letter(board,index,guess):
    for i in index:
        board[i] = guess
    return board
        
        


word = choose_word(wordlist)
guesses = 20
word_length = len(word)

board = create_blank_word(word_length)
print board
print "You have",guesses,"guesses!"
all_guesses = []
while guesses > 0 and check_board(board):
    guesses -= 1
    print board
    print "Past guesses: ", all_guesses
    guess = raw_input("Please guess a letter: ")
    all_guesses.append(guess)
    index = find_letter(word,guess)
    board = board_replace_letter(board,index,guess)
    
print "The word was: ", word

    
    



