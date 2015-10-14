import json

from flask import Flask, Response, request

from blackjack.pitBoss import PitBoss
from blackjack.blackjackObjectEncoder import BlackjackObjectEncoder
from blackjack.model.player import PlayerStates
import config


application = Flask(__name__)

pitBoss = PitBoss()
started = False

# get list of games
@application.route('/games', methods=['GET'])
def get_games():
    return json_response(pitBoss.games.values())


# view game
@application.route('/game/<id>', methods=['GET'])
def get_game(id):
    return json_response(pitBoss.games[id])


# register player
# parameters: name
@application.route('/player', methods=['POST'])
def register_player():
    if started:
        return json_response({'error': 'games have already started'})
    # create player
    player = pitBoss.create_player(request.args.get('name'))

    resp = {}
    resp['player'] = player
    resp['playerId'] = player.id
    resp['location'] = '/player/{}'.format(player.id)

    # search for game to join, create if none exist, then add player
    game = pitBoss.assign_player(player)
    resp['game'] = game
    print 'total players: {}'.format(len(pitBoss.players.values()))

    return json_response(resp)


# view player
@application.route('/player/<id>', methods=['GET'])
def get_player(id):
    return json_response(pitBoss.players[id])


@application.route('/players', methods=['GET'])
def get_players():
    return json_response(pitBoss.players.values())


@application.route('/start', methods=['GET'])
def start_games():
    global started
    pitBoss.start_games()
    started = True
    return json_response({'success': True})


# endpoint for users to check if it's their turn or not
@application.route('/myTurn', methods=['GET'])
def my_turn():
    playerId = request.args.get('playerId')
    myTurn = pitBoss.is_it_my_turn(playerId)
    return json_response({'myTurn': myTurn})


## player actions.
# it must be requesting players turn or these will return an error
@application.route('/setWager', methods=['GET'])
def setWager():
    errorMsg, playerId = check_player(request, PlayerStates.NEEDS_WAGER)
    if errorMsg is not None:
        return json_response({'error': errorMsg})
    wager = request.args.get('wager')
    if wager is None:
        return json_response({'error': 'parameter \"wager\" is required'})
    elif int(wager) < config.MIN_WAGER:
        return json_response({'error': 'wager must be greater than the minimum bet of {}'.format(config.MIN_WAGER)})
    elif int(wager) > pitBoss.players[playerId].chips:
        return json_response({'error': 'you can\'t wager more than you have'})

    pitBoss.set_wager(playerId, int(wager))
    return json_response({'success': True})

# todo hit when wager hasn't been set
@application.route('/hit', methods=['GET'])
def hit():
    errorMsg, playerId = check_player(request, PlayerStates.NEEDS_CARDS)
    if errorMsg is not None:
        return json_response({'error': errorMsg})
    newCard = pitBoss.hit(playerId)
    return json_response(newCard)


@application.route('/doubleDown', methods=['GET'])
def doubleDown():
    errorMsg, playerId = check_player(request, PlayerStates.NEEDS_CARDS)
    if errorMsg is not None:
        return json_response({'error': errorMsg})
    elif len(pitBoss.players[playerId].hand.cards) > 2:
        return json_response({'error': 'you can\'t double down after hitting'})
    newCard = pitBoss.double_down(playerId)
    return json_response(newCard)

@application.route('/stand', methods=['GET'])
def stand():
    errorMsg, playerId = check_player(request, PlayerStates.NEEDS_CARDS)
    if errorMsg is not None:
        return json_response({'error': errorMsg})
    pitBoss.stand(playerId)
    return json_response({'success': True})

@application.route('/surrender', methods=['GET'])
def surrender():
    errorMsg, playerId = check_player(request, PlayerStates.NEEDS_CARDS)
    if errorMsg is not None:
        return json_response({'error': errorMsg})
    elif len(pitBoss.players[playerId].hand.cards) > 2:
        return json_response({'error': 'you can\'t surrender after hitting'})
    pitBoss.surrender(playerId)
    return json_response({'success': True})

# checks to make sure player ID exists, is valid, it is that player's
# turn, and the player is in the provided state
def check_player(request, playerState):
    playerId = request.args.get('playerId')
    if playerId is None:
        return ('parameter "playerId" is required', None)
    elif not playerId in pitBoss.players:
        return ('unknown playerId: {}'.format(playerId), playerId)
    elif not pitBoss.is_it_my_turn(playerId):
        return ('it isn\'t your turn!', playerId)
    elif not pitBoss.players[playerId].state == playerState:
        return ('you\'re not allowed to do that right now', playerId)
    else:
        return (None, playerId)

# helper function for wrapping json in a response
def json_response(obj):
    return Response(json.dumps(obj, cls=BlackjackObjectEncoder, indent=4, separators=(',', ': ')), mimetype='application/json')


if __name__ == '__main__':
    application.run(debug=True)