from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


def comp_choose_word(hand, word_list, n):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    valid_word_dic = {}
    t = n
    while t > 0:
        word_combinations = get_perms(hand, t)
        for i in range(len(word_combinations)):
            if is_valid_word(word_combinations[i], hand, word_list) == True:
                valid_word_dic[word_combinations[i]] = get_word_score(word_combinations[i],n)
        t = t-1
##    if len(valid_word_dic.keys()) > 1:
##        return choice
##    choice = valid_word_dic(valid_word_dic.keys()[0])
##    return choice

    if len(valid_word_dic.keys()) == 0:
        print "No valid words can be formed with the current hand"
        return 0
    choice = keywithmaxval(valid_word_dic)    
    return choice
    #return valid_word_dic
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list, n):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    print "Computers Hand: "
    display_hand(hand)
    choice = comp_choose_word(hand, word_list, n)
    total = 0
    while choice != 0:
        print choice, "earned", get_word_score(choice, n), "points"
        total += get_word_score(choice,n)
        hand = update_hand(hand, choice)
        print "Computers Hand: "
        display_hand(hand)
        choice = comp_choose_word(hand, word_list, n)

    print "No more words possible with this hand:"
    print "Final hand score:  ", total
       
   
   
        
    
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    n = 4
    user = raw_input("Enter 'n' for new hand, 'r' for same hand, 'e' to exit: ")
    while not( user == 'r' or user == 'n' or user == 'e') :
        user = raw_input("Enter 'n' for new hand, 'r' for same hand, 'e' to exit: ")
    horc = raw_input("Enter 'u' for user or 'c' for computer: ")
    while not(horc == 'u' or horc == 'c'):
        print "Invalid entry.  Please read the instrctions"
        horc = raw_input("Enter  'u' for user or 'c'for computer: ")
            
    hand = deal_hand(n)
    while user != 'e':
        if horc == 'c':
            comp_play_hand(hand, word_list, n)    
        else:
            if user == 'n':
                print "Play new hand"
                hand = deal_hand(n)
                old_hand = play_hand(hand, word_list,n)
                
            if user == 'r':
                print "Play old hand"
                old_hand = play_hand(old_hand, word_list,n)
        
        user = raw_input("Enter 'n' for new hand, 'r' for same hand, 'e' to exit: ")
        while not (user == 'r' or user == 'n' or user == 'e'):
            user = raw_input("Enter 'n' for new hand, 'r' for same hand, 'e' to exit: ")
        horc = raw_input("Enter 'u' for user or 'c' for computer: ")
        while not(horc == 'u' or horc == 'c'):
            print "Invalid entry.  Please read the instrctions"
            horc = raw_input("Enter  'u' for user or 'c'for computer: ")
        if horc == 'c' and user == 'r':
            print "All words have been used with the computers old hand."
            print "Choosing new hand"
    print "Game Over!"
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    #n = 6
    hand = deal_hand(n)
    #perms = get_perms(hand,3)
    #choice = comp_choose_word(hand, word_list, n)
    #print choice
    comp_play_hand(hand, word_list, n)
