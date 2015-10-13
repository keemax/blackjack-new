from blackjack.model.card import Card
from blackjack.model.card import Suit
import random

suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]

class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for val in range(1, 14):
                if val > 10:
                    val = 10
                card = Card(suit, val)
                self.cards.append(card)

    def draw_card(self):
        card = random.choice(range(len(self.cards)))
        return self.cards.pop(card)