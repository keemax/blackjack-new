class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.soft = False

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if not self.soft:
            if card.value == 1:
                if self.value <= 11:
                    self.soft = True
        else:
            if self.value > 11:
                self.soft = False