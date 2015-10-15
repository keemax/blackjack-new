from blackjack.model.hand import Hand


class Player:
    def __init__(self, id, name):
        self.id = id
        self.chips = 0
        self.name = name
        self.current_wager = 0
        self.hand = Hand()
        self.state = PlayerStates.NEEDS_WAGER
        self.max_chips = 0
        self.wins = 0

    def add_chips(self, amount):
        self.chips += amount
        if self.chips > self.max_chips:
            self.max_chips = self.chips
        if amount > 0:
            self.wins += 1

    def set_wager(self, wager):
        self.current_wager = wager

class PlayerStates:
    NEEDS_WAGER = 0
    NEEDS_CARDS = 1
    STANDING = 2
    BUSTED = 3