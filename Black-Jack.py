# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    def draw_back(self, canvas, pos):
        if self.suit == 'C' or self.suit == 'S':
            canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        elif self.suit == 'H' or self.suit == 'D':
            canvas.draw_image(card_back, [CARD_CENTER[0] + CARD_SIZE[0], CARD_CENTER[1]], CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    global CARD_SIZE
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        cards_in_hand = ""
        for card in self.cards:
            cards_in_hand += card.suit + card.rank + " "
        return "hand contains " + cards_in_hand

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total = 0
        for card in self.cards:
            for value in VALUES:
                if card.rank == value and card.rank == 'A' and total+10 < 21:
                    total += 10
                elif card.rank == value:    
                    total += VALUES[value]
        return total
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]

    
player = Hand()
dealer = Hand()
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)             
                
    def __str__(self):
        cards_string = ""
        for card in self.cards:
            cards_string += card.suit + card.rank + " "
        return "Deck contains " + cards_string           
    
    def deal_card(self):
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

deck = Deck()
#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, score
    deck = Deck()
    player = Hand()
    dealer = Hand()

    # your code goes here
    deck.shuffle()
    
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    if in_play:
        outcome = "You lost the round!"
        score -= 1
        in_play = True
        
    else:
        in_play = True
        outcome = ""

def hit():
    global in_play, outcome, score, player, dealer, deck
    
    # if the hand is in play, hit the player
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        in_play = False
        outcome =  "You have busted!"
        score -= 1
        

        print "Player: " + str(player.get_value())
        print "Dealer: " + str(dealer.get_value())
    
    
    
        
def stand():
    global in_play, outcome, score, player, dealer, deck
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer.get_value() < 17:
        if in_play:
            dealer.add_card(deck.deal_card())
    
 
    # assign a message to outcome, update in_play and score
    if dealer.get_value() > 21:
        in_play = False
        outcome = "Dealer Busted!"
        score += 1
        

        print "Player: " + str(player.get_value())
        print "Dealer: " + str(dealer.get_value())
        
    else:
        if dealer.get_value() >= player.get_value():
            in_play = False
            outcome = "Dealer wins!"
            score -= 1

            print "Player: " + str(player.get_value())
            print "Dealer: " + str(dealer.get_value())
        else:
            in_play = False
            outcome = "You win!"
            score += 1
            

            print "Player: " + str(player.get_value())
            print "Dealer: " + str(dealer.get_value())
# draw handler    
def draw(canvas):
    global player, dealer, outcome
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text(outcome, (170, 135), 40, 'White', 'serif')
    canvas.draw_text("Score: " + str(score), (10, 30), 30, 'White', 'serif')
    player.draw(canvas, [50, 200])
    dealer.draw(canvas, [50, 400])
    if in_play:
        dealer.cards[0].draw_back(canvas, [50, 400])
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
