from flask.json import JSONEncoder
from blackjack.game import Game
from blackjack.model.player import Player

# encoder for converting classes to json
class BlackjackObjectEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Game):
            return {
                'id': o.id,
                'players': o.players,
                'active': o.active,
                'revealedCards': o.revealed_cards,
                'deckNumber': o.deck_number,
                'dealerUpCard': o.dealer_up_card
            }
        elif isinstance(o, Player):
            return {
                'name': o.name,
                'chips': o.chips,
                'hand': o.hand
            }
        else:
            return o.__dict__