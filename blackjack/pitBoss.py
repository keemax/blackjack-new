import uuid
from blackjack.game import Game
from blackjack.model.player import Player, PlayerStates
import config


class PitBoss:
    def __init__(self):
        self.games = {}
        self.players = {}
        self.playerAssignments = {}

    # creates a new player with the provided name and assigns chips
    def create_player(self, name):
        playerId = str(uuid.uuid4())
        player = Player(playerId, name)
        player.add_chips(config.STARTING_CHIPS)
        self.players[playerId] = player
        print 'created player with ID {}'.format(player.id)
        return player

    # assigns provided player to a game.
    # creates a new game if there are none to join.
    # returns game that the player joined
    def assign_player(self, player):
        game = None
        for gameId, potentialGame in self.games.iteritems():
            if not potentialGame.is_full():
                game = potentialGame
                break
        if game is None:
            gameId = str(uuid.uuid4())
            game = Game(gameId)
            self.games[gameId] = game
            print 'created new game with ID {}'.format(gameId)

        game.add_player(player)
        self.playerAssignments[player.id] = game
        print 'added player {} to game {}'.format(player.id, game.id)
        return game

    def start_games(self):
        for game in self.games.values():
            game.start()

    def set_wager(self, playerId, wager):
        game, player = self.__get_game_and_player(playerId)
        game.set_wager(player, wager)


    def hit(self, playerId):
        game, player = self.__get_game_and_player(playerId)
        return game.hit(player)


    def double_down(self, playerId):
        game, player = self.__get_game_and_player(playerId)
        return game.double_down(player)

    def stand(self, playerId):
        game, player = self.__get_game_and_player(playerId)
        game.stand(player)

    def surrender(self, playerId):
        game, player = self.__get_game_and_player(playerId)
        game.surrender(player)

    def __get_game_and_player(self, playerId):
        game = self.playerAssignments[playerId]
        player = self.players[playerId]
        return (game, player)

    def is_it_my_turn(self, playerId):
        game = self.playerAssignments[playerId]
        if not game.active:
            return False
        return game.players[game.current_player_index].id == playerId and game.active


