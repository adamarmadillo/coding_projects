import random
import math

# define handsize, discards, hands, card ranks and suits
handsize = 8
discards = 3
hands = 4
ranklib = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suitlib = ["C", "D", "H", "S"]
suitname = ["clubs", "diamonds", "hearts", "spades"]
# create the full deck with all combinations of ranks and suits structured as [rank, suit]
# fulldeck is the deck state before discards/plays
fulldeck = [[r, s] for s in suitlib for r in ranklib]

# function to convert suit letter to symbol
def suitsymbol(suit):
    if suit == "C":
        return "♣"
    elif suit == "D":
        return "♦"
    elif suit == "H":
        return "♥"
    elif suit == "S":
        return "♠"
    else:
        return suit

# shorthand turns [9,C] into "9 ♣"
def shorthand(rank, suit):
    return (f"{rank} {suitsymbol(suit)}")

# formats sets of cards
# ([R, S],[R, S]) -> "[R ♣][R ♦]"
def sh_set(cardset):
    # joins the shorthand of each card with [] brackets
    return (f"[{(']['.join([shorthand(cardset[i][0], cardset[i][1]) for i in range(len(cardset))]))}]")

# IMPROVE: can't follow other stored card data
# converts card into a sortable numeric value
def sortvalue(card):
    return (ranklib.index(card[0]) + (suitlib.index(card[1]) * 100))
# converts numeric value back into card
def desortvalue(card):
    return (ranklib[card % 100], suitlib[math.floor(card / 100)])
# card -> number -> sorted numbers -> sorted cards
def cardsort(cardset):
    temp_cardset = [sortvalue(cardset[i]) for i in range(len(cardset))]
    temp_cardset = sorted(temp_cardset)
    return [desortvalue(temp_cardset[i]) for i in range(len(temp_cardset))]

# returns all cards of a specified suit/rank (value) from a deck (deck)
def sh_val(deck, value):
    return (sh_set([deck[i] for i in range(len(deck)) if value in deck[i]]))

# prints the full (sorted) deck split into each suit
def sh_deck(deck):
    return ("\n\n ".join([(sh_val(cardsort(deck), suitlib[i])) for i in range(4)]))


# GAME STRUCTURE
# playgame
#   round
#     turn
#     turn
#     round over
#   shop
#     actions
#   round
#     turn
#     loss
# play again
# playgame

# TEXT FORMAT:
# Question
# You: command
# 
# Answer
# 
# Question
# You: command
# Further question
# You: command
#
# Answer
# 
# Question
# You: command
# 
# Option question
#
# Type cancel etc
# You: command


# turn deck is the deck during the turn
turndeck = fulldeck.copy()
# used deck is empty
useddeck = []

# function to draw up to handsize from turn deck and removes them from turn deck
# only if held hand has less cards than handsize
heldhand = []
def drawhand():
    if len(heldhand) < handsize:
        while (len(heldhand)) < handsize:
            tempcard = random.choice(turndeck)
            heldhand.append(tempcard)
            turndeck.remove(tempcard)
drawhand()
heldhand = cardsort(heldhand)

# hands/discards left is the number of hands/discards left each turn
handsleft = hands
discardsleft = discards

# turn loop start
# actions available each turn: play, discard, view: [(full, turn, used) deck, hand (reorder) suit, rank, jokers (reorder), consumables(use)]
# ACTIONS ACTUALLY CODED: view, reorder

# view function
def viewhand():
    print(f"\nYour hand:\n {sh_set(heldhand)}\n")

def viewdeck():
    print(f"\nYour deck:\n {sh_deck(fulldeck)}\n")

def viewsuit(suit):
    print(f"\nYour cards with {suitname[suitlib.index(suit)]}:\n {sh_val(fulldeck, suit)}\n")

def viewrank(rank):
    print(f"\nYour cards with {rank}:\n{sh_val(fulldeck, rank)}\n")

def view():
    # repeats if invalid input
    while True:
        tempinput = input("What to view? (Type help for options)\nYou: ").lower()
        # ask what you can view (no break to cyle back)
        if tempinput == "help":
            print("\nYour options are: deck, hand, suit, rank")
        # view deck, hand, suit, suit directly, rank, rank directly
        elif tempinput == "deck":
            viewdeck()
            break
        elif tempinput == "hand":
            viewhand()
            break
        elif tempinput == "suit":
            # repeats if invalid input
            while True:
                tempinput = input("What suit? (C, D, H, S)\nYou: ").upper()
                if tempinput in suitlib:
                    viewsuit(tempinput)
                    break
                else:
                    print("\nInvalid input")
            break
        # skip the suit command straight to specific suit
        elif tempinput.upper() in suitlib:
            tempinput = tempinput.upper()
            viewsuit(tempinput)
            break
        elif tempinput == "rank":
            # repeats if invalid input
            while True:
                tempinput = input("What rank? (2-9, T, J, Q, K, A)\nYou: ").upper()
                # view specific rank
                if tempinput in ranklib:
                    viewrank(tempinput)
                    break
                else:
                    print("\nInvalid input")
            break
        # skip the rank command straight to specific rank
        elif tempinput.upper() in ranklib:
            tempinput = tempinput.upper()
            viewrank(tempinput)
            break
        else:
            print("\nInvalid input")

# display the hand for selection of a card
def giveoption(hand):
    return(f"{sh_set(hand)}\n {''.join([f'[ {i} ]' for i in range(1, (len(hand)) + 1)])}")

# discard function
def discard():
    global discardsleft, heldhand, useddeck, turndeck
    # check for discards available
    if discardsleft > 0:
        # 0 = first prompt, 1 = help asked, 2 = cards have been discarded
        askedalready = 0
        # discard ends when >= 5
        cardsdiscarded = 0
        # repeats if invalid input
        while True:
            if cardsdiscarded < 5:    
                # ask what cards to discard
                if askedalready == 0:
                    tempinput = input(f"\nYou may discard {5 - cardsdiscarded} more card(s). Which cards would you like to discard?\n"
                                      f"\n {giveoption(heldhand)}\n\nType cancel to cancel. (Type help if you are confused)\nYou: ").lower()
                # if help has been asked
                elif askedalready == 1:
                    tempinput == input("You: ")
                # if cards have already been discarded
                else:
                    tempinput = input(f"\nYou may discard {5 - cardsdiscarded} more card(s). Type done if done. Which cards would you like to discard?\nYou: ")
                # checks that the discard hasn't starded
                if tempinput == "cancel" and askedalready <= 1:
                    print("")
                    break
                # print help but don't repeat the prompt
                elif tempinput == "help":
                    print("Type the place of the card you would like to discard")
                    askedalready = 1                
                # if the card is valid to discard
                elif tempinput.isdigit() and int(tempinput) <= handsize and int(tempinput) > 0 and cardsdiscarded < 5:
                    tempinput = int(tempinput)
                    if heldhand[tempinput] == ("-","-"):
                        print(f"\nCard already discarded")
                    else:
                        # perform discard card
                        print()
                if tempinput == "done" and askedalready == 2:
                    cardsdiscarded = 5
                else:
                    print("\nInvalid input")
            else:
                # PERFORM DISCARD ACTION
                discardsleft -= 1
                viewhand()
                print(f"you have {discardsleft} discard(s) left")
                break
    else:
        # if no discards are left
        print("No discards left\n")

# reorder the cards by swapping
def reorder():
    global heldhand
    while True:
        tempinput = input(f"\nWhich card would you like to reorder? (1-{handsize})\n"
                          f"\n {giveoption(heldhand)}\n\nType cancel to cancel. (Type help if you are confused)\nYou: ").lower()
        if tempinput.isdigit() and int(tempinput) <= handsize and int(tempinput) > 0:
            while True:
                tempinput = int(tempinput)
                tempinput2 = input(f"Where would you like to swap it? (1-{handsize})\nYou: ")
                if tempinput2.isdigit() and int(tempinput2) <= handsize and int(tempinput2) > 0 and tempinput != tempinput2:
                    tempinput2 = int(tempinput2)
                    tempcard = heldhand[tempinput - 1]
                    heldhand[tempinput - 1] = heldhand[tempinput2 - 1]
                    heldhand[tempinput2 - 1] = tempcard
                    viewhand()
                    break
                elif tempinput2 == "cancel":
                    print("")
                    break
                else:
                    print("\nInvalid input")
            break
        elif tempinput.lower() == "cancel":
            print("")
            break
        elif tempinput.lower() == "help":
            print("Type the place of the card you would like to swap\n")
        else:
            print("\nInvalid input")


def executeturn():
    # global because held hand is modified
    global heldhand, handsleft
    while True:
        tempinput = input("What would you like to do? (Type help for options)\nYou: ").lower()
        if tempinput == "help":
            print("\nYour options are: view, sort, discard")
            break
        elif tempinput == "view":
            view()
            break
        elif tempinput == "sort":
            heldhand = cardsort(heldhand)
            viewhand()
            break
        elif tempinput == "discard":
            discard()
            break
        elif tempinput == "reorder":
            reorder()
            break
        elif tempinput == "yo":
            print("\nfricken packet??\n")
        elif tempinput == "end":
            handsleft = 0
            break
        else:
            print("\nInvalid input")

print("--GAME START--")
viewdeck()
# custom viewhand for -1 line after deck
print(f"Your hand:\n {sh_set(heldhand)}\n")
while handsleft > 0:
    executeturn()
