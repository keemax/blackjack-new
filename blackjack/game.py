from blackjack.model.deck import Deck
from blackjack.model.hand import Hand
from blackjack.model.player import PlayerStates

import config
import time
import threading



class Game:
    def __init__(self, id):
        self.id = id
        self.deck = Deck()
        self.players = []
        self.current_player_index = 0
        self.active = False
        self.last_move_time = 0
        self.players_with_wagers = 0
        self.revealed_cards = []
        self.deck_number = 0
        self.dealer_up_card = None
        self.dealer_hand = Hand()
        self.round = 0


    def add_player(self, player):
        self.players.append(player)

    def is_full(self):
        return len(self.players) == config.MAX_PLAYERS

    def start(self):
        self.active = True
        self.last_move_time = time.time()
        gameMonitor = threading.Thread(target=monitor_players, args=(self,))
        gameMonitor.start()
        print 'starting game {}'.format(self.id)

    def deal(self):
        for player in self.players:
            print '{}: {}'.format(player.name, player.chips)
        # check deck size
        if len(self.deck.cards) < config.MIN_DECK_SIZE:
            self.deck = Deck()
            self.deck_number += 1
            self.revealed_cards = []

        self.__deal_one_round()
        self.dealer_hand.add_card(self.deck.draw_card())
        self.__deal_one_round()
        self.dealer_up_card = self.deck.draw_card()
        self.revealed_cards.append(self.dealer_up_card)
        self.dealer_hand.add_card(self.dealer_up_card)


    def __deal_one_round(self):
        for player in self.players:
            card = self.deck.draw_card()
            player.hand.add_card(card)
            self.revealed_cards.append(card)

    def end(self):
        self.active = False


    def set_wager(self, player, wager):
        player.set_wager(wager)
        player.state = PlayerStates.NEEDS_CARDS
        self.players_with_wagers += 1
        if self.players_with_wagers == len(self.players):
            self.deal()
            self.players_with_wagers = 0
        self.advance_player()

    def hit(self, player):
        card = self.deck.draw_card()
        self.revealed_cards.append(card)
        player.hand.add_card(card)
        if player.hand.value > 21:
            player.state = PlayerStates.BUSTED
            self.advance_player()
            if self.current_player_index == 0:
                self.__resolve_round()
        return card

    def double_down(self, player):
        card = self.deck.draw_card()
        self.revealed_cards.append(card)
        player.hand.add_card(card)
        player.current_wager = player.current_wager * 2
        if player.hand.value > 21:
            player.state = PlayerStates.BUSTED
        else:
            player.state = PlayerStates.STANDING
        self.advance_player()
        if self.current_player_index == 0:
            self.__resolve_round()
        return card

    def stand(self, player):
        player.state = PlayerStates.STANDING
        self.advance_player()
        if self.current_player_index == 0:
            self.__resolve_round()

    def surrender(self, player):
        player.current_wager = player.current_wager / 2
        player.state = PlayerStates.BUSTED
        self.advance_player()
        if self.current_player_index == 0:
            self.__resolve_round()


    def __resolve_round(self):
        self.__resolve_dealer_hand()
        for player in self.players:
            if player.state == PlayerStates.BUSTED:
                player.chips -= player.current_wager
                player.current_wager = 0
            else:
                self.__resolve_winnings(player, self.dealer_hand)

            player.state = PlayerStates.NEEDS_WAGER
            player.hand = Hand()

        # remove players with insufficient chips
        self.players = filter(lambda player: player.chips >= config.MIN_WAGER, self.players)
        self.dealer_hand = Hand()
        self.round += 1
        if self.round == config.MAX_ROUNDS or len(self.players) == 0:
            self.end()


    def __resolve_dealer_hand(self):
        dealerHand = self.dealer_hand
        dealerDownCard = dealerHand.cards[0]
        self.revealed_cards.append(dealerDownCard)
        while (dealerHand.soft and dealerHand.value < 8) or (not dealerHand.soft and dealerHand.value < 17):
            card = self.deck.draw_card()
            self.revealed_cards.append(card)
            dealerHand.add_card(card)

    def __resolve_winnings(self, player, dealerHand):
        dealerValue = self.dealer_hand.value
        if self.dealer_hand.soft:
            dealerValue += 10

        if player.hand.value == 21 and len(player.hand.cards) == 2:
            if not (dealerValue == 21 and len(dealerHand.cards) == 2):
                player.chips += player.current_wager * 1.5
        elif dealerValue > 21 or player.hand.value > dealerValue:
            player.chips += player.current_wager
        elif player.hand.value < dealerValue:
            player.chips -= player.current_wager
        player.current_wager = 0

    def kick_current_player(self):
        print 'kicking player {}'.format(self.current_player_index)
        self.players.pop(self.current_player_index)
        if self.current_player_index == len(self.players):
            self.current_player_index = 0
        if len(self.players) == 0:
            self.end()

    def advance_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.last_move_time = time.time()


# checks how longs it's been since the last move and kicks inactive players from the game in 1 second intervals
def monitor_players(game):
    while game.active:
        if time.time() - game.last_move_time > config.KICK_TIMEOUT:
            game.kick_current_player()
            if len(game.players) == 0:
                game.end()
        time.sleep(1)