"""random module is used to shuffle the deck

inspect module is used to check which function is calling the print board function, which
determines which version of the board to print

sleep is used to pause the program between board/text outputs to make it seem more like
a person is acting as the dealer and to give the user time to read the text outputs"""
import random
import inspect
from time import sleep

"""Blackjack game made with python

The goal of the game is to get as close to 21 as possible without going over.
It is players (up to 4) vs dealer. The players are dealt two cards face up,
and the dealer gets 1 card face up and 1 face down. Each player chooses "hit"
or "stay" to get another card or stop receiving cards.

If a player is dealt 21, this is a "natural" and the player wins 1.5x the bet
if the dealer does not also have a natural. When the dealer is dealt a 10 card
or Ace, they check the face down card to see if they have a natural. If so, bets
are taken from players without naturals, and players with naturals take a round tie.

If the sum of the inital cards dealt to a player is 9, 10, or 11, the player can
choose to "double down". The player doubles their bet and gets one hit,
then automatically stays.

If a both of a player's initial cards are the same denomination (not rank), they can
choose to "split" their hand into 2 hands. The player automatically places a bet equal
to their original bet, they are not allowed to bet if they don't have enough in
their bankroll.The player must play each hand completely before moving to other.
If the player splits on a pair of Aces, they only get 1 hit per hand, then automatically
stand. Getting a 10 card dealt to one of these Aces does NOT count as a natural.

If the dealer's showing card is an Ace, any player can place an "insurance" side-bet
of up to 1/2 the original bet. This bet is that the dealer's face down card is
a 10 card. If so, insurance betters get 2 * side-bet back, so they would
break even if they bet 1/2 their original bet.

If a player goes over 21 while hitting, they "bust" and the dealer wins and takes
their bet. If a player chooses to stay while still under 21, the dealer then hits up
to 17 until he either beats the player or busts resulting in the player winning and
taking his bet in winnings. All face cards are equal to 10. Ace is equal to 11 or 1,
whichever benefits the player. A tie results in no chips won or lost."""

print("Let's play Blackjack!\n")
CLEAR = "\n" * 20

def print_board():
    """this function prints the updated board after every move and determines whether
    to show the dealers hidden card or not depending on what point the game is at"""

    print("\n" * 7)
    print("DEALER\n")

    line_by_line = [[], [], [], [], []]

    #print dealer cards
    #if the function is called from dealer_move, the cards are all revealed
    # if it is called from anywhere else, the second card is hidden
    if inspect.stack()[1][3] in ("dealer_move", "print_board_natural"):
        for card in GAME_DEALER.hand:
            line_by_line[0].append(ASCII_TEMPLATE[0])
            line_by_line[1].append(ASCII_TEMPLATE[1].format(ASCII_LABELS_TOP[card.rank]))
            line_by_line[2].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[card.suit]))
            line_by_line[3].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[card.suit]))
            line_by_line[4].append(ASCII_TEMPLATE[3].format(ASCII_LABELS_BOTTOM[card.rank]))

    else:
        line_by_line[0].append(ASCII_TEMPLATE[0])
        line_by_line[1].append(ASCII_TEMPLATE[1].format(ASCII_LABELS_TOP[GAME_DEALER.hand[0].rank]))
        line_by_line[2].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[GAME_DEALER.hand[0].suit]))
        line_by_line[3].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[GAME_DEALER.hand[0].suit]))
        line_by_line[4].append(ASCII_TEMPLATE[3].format(ASCII_LABELS_BOTTOM[GAME_DEALER.hand[0].rank]))

        line_by_line[0].append(ASCII_TEMPLATE[0])
        line_by_line[1].append(ASCII_TEMPLATE[1].format("# "))
        line_by_line[2].append(ASCII_TEMPLATE[2].format(" "))
        line_by_line[3].append(ASCII_TEMPLATE[2].format(" "))
        line_by_line[4].append(ASCII_TEMPLATE[3].format("_#"))

    #join method prints the lines of the cards as strings concatenated by a space, not arrays
    for line in line_by_line:
        print(" ".join(line))


    print("""
       _____
     _|___  |
    |     | |
    |     | |
    |     |_|
    |_____|

    Bet: """ + str(GAME_CHIPS.bet) + "\n")

    line_by_line = [[], [], [], [], []]
    line_by_line_split_hand = [[], [], [], [], []]

    #print player cards
    for card in GAME_PLAYER.hand:
        line_by_line[0].append(ASCII_TEMPLATE[0])
        line_by_line[1].append(ASCII_TEMPLATE[1].format(ASCII_LABELS_TOP[card.rank]))
        line_by_line[2].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[card.suit]))
        line_by_line[3].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[card.suit]))
        line_by_line[4].append(ASCII_TEMPLATE[3].format(ASCII_LABELS_BOTTOM[card.rank]))

    for card in GAME_PLAYER.split_hand:
        line_by_line_split_hand[0].append(ASCII_TEMPLATE[0])
        line_by_line_split_hand[1].append(ASCII_TEMPLATE[1].format(ASCII_LABELS_TOP[card.rank]))
        line_by_line_split_hand[2].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[card.suit]))
        line_by_line_split_hand[3].append(ASCII_TEMPLATE[2].format(ASCII_SUITS[card.suit]))
        line_by_line_split_hand[4].append(ASCII_TEMPLATE[3].format(ASCII_LABELS_BOTTOM[card.rank]))

    for line in line_by_line:
        print(" ".join(line))

    for s_line in line_by_line_split_hand:
        print(" ".join(s_line))

    print("\nPLAYER: " + str(GAME_CHIPS.bankroll) + "\n")

"""separate top and bottom labels because 10 is 2 characters long,
so we need to add back that space on the others so the spacing stays the same"""
ASCII_LABELS_TOP = {"Ace": "A ", "Two": "2 ", "Three": "3 ", "Four": "4 ", "Five": "5 ",
                    "Six": "6 ", "Seven": "7 ", "Eight": "8 ", "Nine": "9 ", "Ten": "10",
                    "Jack": "J ", "Queen": "Q ", "King": "K "}

ASCII_LABELS_BOTTOM = {"Ace": "_A", "Two": "_2", "Three": "_3", "Four": "_4", "Five": "_5",
                       "Six": "_6", "Seven": "_7", "Eight": "_8", "Nine": "_9", "Ten": "10",
                       "Jack": "_J", "Queen": "_Q", "King": "_K"}

ASCII_SUITS = {"Hearts": "♥", "Diamonds": "♦", "Spades": "♠", "Clubs": "♣"}

ASCII_TEMPLATE = [
    " _____ ",
    "|{}   |",
    "|  {}  |",
    "|___{}|"
]

#global variables used to make the cards and deck
SUITS = ["Hearts", "Diamonds", "Spades", "Clubs"]
RANKS = ["Ace", "Two", "Three", "Four", "Five", "Six",
         "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

#dictionary to look up corresponding rank to value, not used directly in any classes
VALUES = {"Ace": 11, "Two": 2, "Three": 3, "Four": 4,
          "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9,
          "Ten": 10, "Jack": 10, "Queen": 10, "King": 10}

class Chips:
    """chips class for each player, tracks the bankroll and bets and is not reset between rounds"""

    def __init__(self, bankroll=100):
        self.bankroll = bankroll
        self.bet = 0
        self.insurance_bet = 0
        self.split_bet = 0

    def __str__(self):
        """when chips is printed, this will show"""
        return "PLAYER has: " + str(self.bankroll) + " chips."

    def lose_bet(self):
        """removes the bet from the bankroll if the player loses"""
        self.bankroll -= self.bet

    def win_bet(self):
        """adds the bet to the bankroll if the player wins"""
        self.bankroll += self.bet

    def lose_insurance_bet(self):
        """removes the insurance bet from the bankroll if the dealer does not have 21"""
        self.bankroll -= self.insurance_bet

    def win_insurance_bet(self):
        """adds twice the insurance bet to the bankroll if the dealer does have 21"""
        self.bankroll += self.insurance_bet * 2

    def lose_split_bet(self):
        """removes the split bet amount from the bankroll if the player loses the split hand"""
        self.bankroll -= self.split_bet

    def win_split_bet(self):
        """adds the split bet amount to the bankroll if the player wins the split hand"""
        self.bankroll += self.split_bet

    def win_blackjack(self):
        """adds 1.5x the bet to the bankroll if the player gets a natural blackjack,
        must use int() on self.bet here or else it will get turned into float"""
        self.bankroll += int(self.bet * 1.5)

"""creates an instance of player for each player BEFORE the loop,
so their chips do not get reset"""
#num_players = int(input("How many players? (1-4) "))
GAME_CHIPS = Chips()

"""controls initial game setup (creating deck and shuffling, taking bet,
dealing initial cards, creating player deck and dealer instances).
Game restarts from here in case of replay"""
while True:

    #global gameover variable that controls the while loop for the game
    GAMEOVER = False

    class Card:
        """card class that gets appended to the deck in every configuration"""
        def __init__(self, suit, rank):
            """suit and rank only, values dict is only for looking up value"""
            self.suit = suit
            self.rank = rank

        def __str__(self):
            """str method that returns a logical, readable string with rank and suit"""
            return self.rank + " of " + self.suit

        def __int__(self):
            """returns the rank of the card as an integer"""
            return VALUES[self.rank]

    class Deck:
        """deck class containing 52 cards, A-K in 4 suits"""
        def __init__(self):
            """goes through each rank in each suit, creates a card and appends to deck"""
            
            self.deck = []
            """
            for suit in SUITS:
                for rank in RANKS:
                    self.deck.append(Card(suit, rank))
            """
            self.deck.append(Card("Hearts", "Five"))
            self.deck.append(Card("Diamonds", "Five"))
            self.deck.append(Card("Spades", "Five"))
            self.deck.append(Card("Clubs", "Five"))
            self.deck.append(Card("Hearts", "Six"))
            self.deck.append(Card("Diamonds", "Six"))
            self.deck.append(Card("Spades", "Six"))
            self.deck.append(Card("Clubs", "Six"))
            self.deck.append(Card("Hearts", "Ten"))
            self.deck.append(Card("Diamonds", "Ten"))
            self.deck.append(Card("Spades", "Ten"))
            self.deck.append(Card("Clubs", "Ten"))

        def __str__(self):
            """str method in case we want to print whole deck for debugging,
            adds each card in deck to deck_string with a new line separating each card"""
            deck_string = ""
            for card in self.deck:
                deck_string += "\n" + card.__str__()
            return "Deck List: " + deck_string

        def shuffle_deck(self):
            """shuffles the deck using the shuffle function from the random module"""
            random.shuffle(self.deck)

        def deal_card(self):
            """method to deal the top card from the deck, used with hit()"""
            return self.deck.pop()

    class Player:
        """player class, tracks hand and is reset each round"""
        def __init__(self):
            #empty array to add cards to during gameplay
            #sum is the sum of all cards in players hand
            #aces is the number of aces
            self.hand = []
            self.sum = 0
            self.split_hand = []
            self.split_sum = 0
            self.aces = 0
            self.split_or_double = False

        def __str__(self):
            """method to let player be printed, shows the cards in the player's hand, and
            iterates through list of cards in hand to dislpay as string here"""
            hand_string = ""
            for card in self.hand:
                hand_string += str(card) + "\n"
            return "\nPLAYER has: \n" + hand_string + "\n" + "and" + str(self.bankroll) + "chips."

        def hit(self, card):
            """this method adds a card to the hand"""
            self.hand.append(card)
            self.sum += VALUES[card.rank]

            #adds 1 to the aces count if the new card is an ace
            if card.rank == "Ace":
                self.aces += 1

        def split_hit(self, card):
            """this method adds a card to the split hand"""
            self.split_hand.append(card)
            self.split_sum += VALUES[card.rank]

            if card.rank == "Ace":
                self.aces += 1

        def decide_ace(self):
            """this decides whether ace being 1 or 11 is better for the player.
            If the sum is over 21 and there are aces remaining to be accounted for in the hand,
            then we subtract 10 from the sum (essentially making an 11 ace a 1) and then
            remove the ace from the aces count"""
            while self.sum > 21 and self.aces:
                self.sum -= 10
                self.aces -= 1

            while self.split_sum > 21 and self.aces:
                self.split_sum -= 10
                self.aces -= 1

    #create instances of the classes we need for the game
    #inside loop, so reset upon game replay
    GAME_DECK = Deck()
    GAME_DEALER = Player()
    GAME_PLAYER = Player()

    def get_bet(chips):
        """function that gets input from player for bet amount, checks if it is a valid number,
        and checks if it is less than the total chips in bank"""
        while True:
            try:
                chips.bet = int(input("How much would you like to bet? "))
            except (TypeError, ValueError):
                print("Not valid, must enter an integer.\n")
            else:
                if chips.bet <= GAME_CHIPS.bankroll and chips.bet > 0:
                    GAME_CHIPS.bet = chips.bet
                    print("\nYou bet " + str(chips.bet) + " chips!\n")
                    break
                else:
                    print("You cannot bet this much!\n")

    def get_move():
        """function asks for move decision, checks if it is valid and
        either deals another card or ends the player's turn. Once the player
        stays or a bust or blackjack occurs, the loop ends."""
        while True:

            if GAME_PLAYER.sum > 21:
                print("Player busts! Dealer wins!\n")
                GAME_CHIPS.lose_bet()
                break
            elif GAME_PLAYER.sum == 21:
                print("Player got BLACKJACK!\n")
                GAME_CHIPS.win_blackjack()
                break

            move_selection = input("Do you want to hit or stay? ")

            if move_selection.lower() in ("hit", "h"):
                GAME_PLAYER.hit(GAME_DECK.deal_card())
                GAME_PLAYER.decide_ace()
                print_board()
                continue
            elif move_selection.lower() in ("stay", "s"):
                break

            print("Invalid answer. Must enter 'hit' or 'stay'. \n")

    def split_get_move(which_sum, which_hand):
        """function called when player splits on a non-Ace pair,
        plays out the hand passed in as a parameter"""
        while True:

            if which_sum > 21:
                print("Player busts! You lose this hand.\n")
                GAME_CHIPS.lose_bet()
                break
            elif which_sum == 21:
                print("Player got BLACKJACK!\n")
                GAME_CHIPS.win_blackjack()
                break

            move_selection = input("Do you want to hit or stay? ")

            if move_selection.lower() in ("hit", "h"):
                if which_hand[0] == GAME_PLAYER.hand[0]:
                    GAME_PLAYER.hit(GAME_DECK.deal_card())
                    GAME_PLAYER.decide_ace()
                    print_board()
                    which_sum = GAME_PLAYER.sum
                    which_hand = GAME_PLAYER.hand
                else:
                    GAME_PLAYER.split_hit(GAME_DECK.deal_card())
                    GAME_PLAYER.decide_ace()
                    print_board()
                    which_sum = GAME_PLAYER.split_sum
                    which_hand = GAME_PLAYER.split_hand
                continue
            elif move_selection.lower() in ("stay", "s"):
                break

            print("Invalid answer. Must enter 'hit' or 'stay'. \n")

    def dealer_move():
        """performs dealer moves after player has stayed,
        adds cards to dealers hand up to 17 or over player"""

        print_board()
        sleep(1)

        while GAME_DEALER.sum < 17 and GAME_DEALER.sum <= GAME_PLAYER.sum:
            GAME_DEALER.hit(GAME_DECK.deal_card())
            GAME_DEALER.decide_ace()
            print_board()
            sleep(1)
        if GAME_DEALER.sum > 21:
            print("Dealer busts! Player wins!\n")
            GAME_CHIPS.win_bet()
        elif GAME_DEALER.sum == 21:
            print("Dealer got BLACKJACK!\n")
            GAME_CHIPS.lose_bet()
        elif GAME_DEALER.sum == GAME_PLAYER.sum:
            print("Round tied!\n")
        elif GAME_DEALER.sum < GAME_PLAYER.sum:
            print("Player got closer to 21! Player wins!\n")
            GAME_CHIPS.win_bet()
        else:
            print("Dealer got closer to 21! Dealer wins!\n")
            GAME_CHIPS.lose_bet()

    def print_board_natural():
        """exists so it can be inspected from within the print board
        function to see which version of the board to print"""
        sleep(1)
        print_board()

    def double_down():
        """checks if any player has initial cards totaling 9,10 or 11,
        and if so asks if they want to double their bet"""
        if GAME_PLAYER.sum in (9, 10, 11):
            while True:
                double_down_input = input("Do you want to double down? ").lower()
                if double_down_input in ("yes", "y", "no", "n"):
                    break
                print("Invalid answer. Please enter yes, no, y or n.\n")

            if double_down_input in ("yes", "y"):
                #checks if the player has enough chips to double down
                if GAME_CHIPS.bankroll >= GAME_CHIPS.bet * 2:
                    GAME_PLAYER.split_or_double = True
                    GAME_CHIPS.bet *= 2
                    #if player doubled down, they get 1 additional card only, then dealer goes
                    GAME_PLAYER.hit(GAME_DECK.deal_card())
                    GAME_PLAYER.decide_ace()
                    print_board()
                    if GAME_PLAYER.sum == 21:
                        print("Player got BLACKJACK! Player wins 1.5x their bet!")
                        GAME_CHIPS.win_blackjack()
                else:
                    print("You don't have the funds to double down!\n")

    def split():
        """checks if any player has a pair, asks if they want to split their hand"""
        if GAME_PLAYER.hand[0].rank == GAME_PLAYER.hand[1].rank and len(GAME_PLAYER.hand) == 2:
            while True:
                split_input = input("Do you want to split your hand? You must bet equally on the second hand. ").lower()
                if split_input in ("yes", "y", "no", "n"):
                    break
                print("Invalid answer. Please enter yes, no, y or n.\n")

            """if yes, this pops the second card off the players hand and appends it
            to the split hand, then it re-adjusts the sums of the two hands"""
            if split_input in ("yes", "y"):
                #checks if the player has enough chips to split
                if GAME_CHIPS.bankroll >= GAME_CHIPS.bet * 2:
                    GAME_PLAYER.split_or_double = True
                    split_card = GAME_PLAYER.hand.pop()
                    GAME_PLAYER.split_hand.append(split_card)
                    GAME_PLAYER.split_sum = VALUES[split_card.rank]
                    GAME_PLAYER.sum -= VALUES[split_card.rank]
                    GAME_CHIPS.split_bet = GAME_CHIPS.bet
                    print_board()
                else:
                    print("You don't have the funds to split this hand!\n")

            #then play each hand all the way through separately
            #if the player split on a pair of aces, only 1 card is dealt to each hand
            if GAME_PLAYER.hand[0].rank == "Ace":
                GAME_PLAYER.hit(GAME_DECK.deal_card())
                GAME_PLAYER.split_hit(GAME_DECK.deal_card())
                GAME_PLAYER.decide_ace()
                print_board()
            else:
            #if the player split on any other pair, the round is fully played out for first hand before moving to split hand
                split_get_move(GAME_PLAYER.sum, GAME_PLAYER.hand)
                print("Now playing the split hand...")
                split_get_move(GAME_PLAYER.split_sum, GAME_PLAYER.split_hand)
                #if one or both hands haven't busted or got 21, dealer moves and reports outcome
                if GAME_PLAYER.sum < 21 or GAME_PLAYER.split_sum < 21:
                    dealer_move()
                GAMEOVER = True

    def insurance():
        """checks if the dealer's face up card is an Ace, and if so asks player
        if they want to place an insurance bet, then checks if the bet is valid
        (up to 1/2 of their original bet) and stores it in separate variable"""
        if GAME_DEALER.hand[0].rank == "Ace":
            while True:
                try:
                    insurance_input = input("Do you want to place an insurance bet? ").lower()
                except (TypeError, ValueError):
                    print("Invalid answer. Please enter yes, no, y or n.\n")
                else:
                    if insurance_input in ("yes", "y", "no", "n"):
                        break
                print("Invalid answer. Please enter yes, no, y or n.\n")

            if insurance_input in ("yes", "y"):
                if GAME_CHIPS.bankroll - GAME_CHIPS.bet > 0:
                    while True:
                        try:
                            insurance_num = int(input("\nHow many chips do you want to bet? You can bet up to half of your original bet. "))
                        except (TypeError, ValueError):
                            print("Not valid, must enter an integer.\n")
                        else:
                            #if the insurance num given is between 0 and 1/2 the original bet, and if the player has enough chips for both bets
                            if 0 < insurance_num <= int(GAME_CHIPS.bet / 2) and GAME_CHIPS.bankroll - GAME_CHIPS.bet >= insurance_num:
                                GAME_CHIPS.insurance_bet = insurance_num
                                sleep(0.6)
                                print("\nYou placed an insurance bet of " + str(insurance_num) + " chips!\n")
                                sleep(0.6)
                                break
                            else:
                                print("You cannot bet this much!\n")

                    #if the value of the dealer's other card is 10, give the player their insurance bet
                    if VALUES[GAME_DEALER.hand[1].rank] == 10:
                        GAME_CHIPS.win_insurance_bet()
                        print("Dealer had a ten-card!\n")
                        sleep(0.6)
                        print("But at least you got insurance!\n")
                        sleep(0.6)
                    else:
                        GAME_CHIPS.lose_insurance_bet()
                        print("Dealer did not have a ten-card.\n")
                        sleep(0.6)
                        print("You lost your insurance bet.\n")
                        sleep(0.6)
                else:
                    print("You don't have the funds to place an insurance bet!\n")
                    sleep(0.6)

    #initial deck shuffling, and before each new round
    GAME_DECK.shuffle_deck()

    #deal initial 2 cards to player
    GAME_PLAYER.hit(GAME_DECK.deal_card())
    GAME_PLAYER.hit(GAME_DECK.deal_card())
    #decide ace function in case both cards dealt are aces, total would be 22
    GAME_PLAYER.decide_ace()

    #deal 2 cards to dealer, 1 face down
    GAME_DEALER.hit(GAME_DECK.deal_card())
    GAME_DEALER.hit(GAME_DECK.deal_card())
    GAME_DEALER.decide_ace()

    #get the bet from the player
    print("PLAYER has " + str(GAME_CHIPS.bankroll) + " chips to play with.\n")
    get_bet(GAME_CHIPS)

    #tell the player what cards they have, and the dealers one face up card
    print_board()

    #this loop controls the player's turn and goes until someone wins
    while not GAMEOVER:

        #check for requirements to make insurance bet and ask
        insurance()

        """checking for naturals
        cannot be in its own function because the break statements
        need to refer to the gameover while loop"""
        if GAME_DEALER.sum == GAME_PLAYER.sum and GAME_DEALER.sum == 21:
            #shows board with dealers card exposed if dealer gets a natural
            print_board_natural()
            print("Player and Dealer both got 21! Round tied!\n")
            break
        elif GAME_PLAYER.sum == 21:
            print("Player got 21! Player wins!\n")
            GAME_CHIPS.win_blackjack()
            break
        elif GAME_DEALER.sum == 21:
            print_board_natural()
            print("Dealer got 21! Dealer wins!\n")
            GAME_CHIPS.lose_bet()
            break

        #checks for special hand (5,5)
        if GAME_PLAYER.hand[0].rank == "Five" and GAME_PLAYER.hand[1].rank == "Five":
            print("\nYou have the unique hand (5,5), the only hand which has the "
                  "option to double down as well as split. BUT, you may only do one of them.\n")

        #checks for special cases and asks player if they want to use them
        double_down()
        split()

        #after natural check and special cases input, gets player's move
        if not GAME_PLAYER.split_or_double:
            get_move()

        #if player did not bust or get 21, dealer moves
        if GAME_PLAYER.sum < 21 or 0 < GAME_PLAYER.split_sum < 21:
            dealer_move()
        GAMEOVER = True
        break

    #if player has no chips left, asks if they want to buy more to keep game going
    if GAME_CHIPS.bankroll == 0:

        while True:
            MORE_CHIPS = input("You don't have any chips left! Buy more? ").lower()
            if MORE_CHIPS in ("yes", "y", "no", "n"):
                break
            print("Invalid answer. Please enter yes, no, y or n.\n")

        #if player wants more chips, ask how many and check if answer is within range and valid
        if MORE_CHIPS in ("yes", "y"):
            while True:
                try:
                    CHIPS_BUY = int(input("How many chips would you like to buy? (1-1000) "))
                except (TypeError, ValueError):
                    print("Not valid, must enter an integer.\n")
                else:
                    if 1 <= CHIPS_BUY <= 1000:
                        GAME_CHIPS.bankroll = CHIPS_BUY
                        print("\nYou bought " + str(CHIPS_BUY) + " more chips!\n")
                        break
                    else:
                        print("You cannot buy this amount!\n")

            #resets attributes of chips that are checked in other parts of the program to prevent bugs
            GAME_CHIPS.split_bet = 0
            GAME_CHIPS.insurance_bet = 0
            print(CLEAR)
            continue
        else:
            print("Powering down...")
            break
    else:
        #asks user if they want to play again, waits for valid input
        while True:
            RESPONSE = input("Want to play again? ").lower()
            if RESPONSE in ("yes", "y", "no", "n"):
                break
            print("Invalid answer.\n")

        #either resets player's hand or shuts down program.
        if RESPONSE in ("yes", "y"):
            print(CLEAR)
            GAME_CHIPS.split_bet = 0
            GAME_CHIPS.insurance_bet = 0
            continue
        else:
            print("Powering down...")
            break
