import unittest
import application
import json
import config

# tests against server with no players or games yet
class BlackjackEmptyTestCase(unittest.TestCase):

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()

    def test_start(self):
        rv = self.app.get('/start')
        assert 'no games yet' in rv.data

    def test_get_games(self):
        rv = self.app.get('/games')
        games = json.loads(rv.data)
        assert len(games) == 0

    def test_get_invalid_game(self):
        rv = self.app.get('/game/thisdoesnotexist')
        assert 'unknown gameId' in rv.data

    def test_get_players(self):
        rv = self.app.get('/players')
        players = json.loads(rv.data)
        assert len(players) == 0

    def test_get_invalid_player(self):
        rv = self.app.get('/player/thisdoesnotexist')
        assert 'unknown playerId' in rv.data

    def test_my_turn_no_player_id(self):
        rv = self.app.get('/myTurn')
        assert 'parameter playerId is required' in rv.data

    def test_my_turn_invalid_player_id(self):
        rv = self.app.get('/myTurn?playerId=thisdoesnotexist')
        assert 'unknown playerId' in rv.data

    def test_set_wager_no_player_id(self):
        rv = self.app.get('/setWager')
        assert 'parameter playerId is required' in rv.data

    def test_set_wager_invalid_player_id(self):
        rv = self.app.get('/setWager?playerId=thisdoesnotexist')
        assert 'unknown playerId' in rv.data

    def test_hit_no_player_id(self):
        rv = self.app.get('/hit')
        assert 'parameter playerId is required' in rv.data

    def test_hit_invalid_player_id(self):
        rv = self.app.get('/hit?playerId=thisdoesnotexist')
        assert 'unknown playerId' in rv.data

    def test_double_down_no_player_id(self):
        rv = self.app.get('/doubleDown')
        assert 'parameter playerId is required' in rv.data

    def test_double_down_invalid_player_id(self):
        rv = self.app.get('/doubleDown?playerId=thisdoesnotexist')
        assert 'unknown playerId' in rv.data

    def test_stand_no_player_id(self):
        rv = self.app.get('/stand')
        assert 'parameter playerId is required' in rv.data

    def test_stand_invalid_player_id(self):
        rv = self.app.get('/stand?playerId=thisdoesnotexist')
        assert 'unknown playerId' in rv.data

    def test_surrender_no_player_id(self):
        rv = self.app.get('/surrender')
        assert 'parameter playerId is required' in rv.data

    def test_surrender_invalid_player_id(self):
        rv = self.app.get('/surrender?playerId=thisdoesnotexist')
        assert 'unknown playerId' in rv.data


# tests with a registered player but the game hasn't started
class BlackjackOnePlayerNotStartedTestCase(unittest.TestCase):
    name = 'max'

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()
        rv = self.app.post('/player?name={}'.format(self.name))
        startInfo = json.loads(rv.data)
        self.playerId = startInfo['playerId']
        self.gameId = startInfo['game']['id']

    def tearDown(self):
        self.app.get('/reset')

    def test_get_games(self):
        rv = self.app.get('/games')
        games = json.loads(rv.data)
        assert len(games) == 1

    def test_get_game(self):
        rv = self.app.get('/game/{}'.format(self.gameId))
        game = json.loads(rv.data)
        assert game['id'] == self.gameId
        assert len(game['players']) == 1
        assert not game['active']

    def test_get_players(self):
        rv = self.app.get('/players')
        players = json.loads(rv.data)
        assert len(players) == 1

    def test_get_player(self):
        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        assert player['name'] == self.name
        assert player['chips'] == config.STARTING_CHIPS
        playerHand = player['hand']
        assert len(playerHand['cards']) == 0
        assert playerHand['value'] == 0
        assert not playerHand['soft']

    def test_create_player(self):
        rv = self.app.post('/player?name=player2')
        startInfo = json.loads(rv.data)
        assert startInfo['playerId'] != self.playerId
        assert startInfo['game']['id'] == self.gameId
        rv = self.app.get('/players')
        players = json.loads(rv.data)
        assert len(players) == 2

    def test_start(self):
        rv = self.app.get('/start')
        startResp = json.loads(rv.data)
        assert startResp['success']

    def test_my_turn(self):
        rv = self.app.get('/myTurn?playerId={}'.format(self.playerId))
        myTurn = json.loads(rv.data)
        assert not myTurn['myTurn']

    def test_set_wager_no_wager(self):
        rv = self.app.get('/setWager?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_set_wager(self):
        rv = self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, 10))
        assert 'it isn\'t your turn' in rv.data

    def test_hit(self):
        rv = self.app.get('/hit?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_double_down(self):
        rv = self.app.get('/doubleDown?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_stand(self):
        rv = self.app.get('/stand?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_surrender(self):
        rv = self.app.get('/surrender?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data


class BlackjackOnePlayerStartTestCase(unittest.TestCase):
    name = 'max'

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()
        rv = self.app.post('/player?name={}'.format(self.name))
        startInfo = json.loads(rv.data)
        self.playerId = startInfo['playerId']
        self.gameId = startInfo['game']['id']
        self.app.get('/start')

    def tearDown(self):
        self.app.get('/reset')

    def test_get_game(self):
        rv = self.app.get('/game/{}'.format(self.gameId))
        game = json.loads(rv.data)
        assert game['id'] == self.gameId
        assert len(game['players']) == 1
        assert game['active']

    def test_create_player(self):
        rv = self.app.post('/player?name=blah')
        assert 'games have already started' in rv.data

    def test_start(self):
        rv = self.app.get('/start')
        assert 'already started' in rv.data

    def test_my_turn(self):
        rv = self.app.get('/myTurn?playerId={}'.format(self.playerId))
        myTurn = json.loads(rv.data)
        assert myTurn['myTurn']

    def test_set_wager_no_wager(self):
        rv = self.app.get('/setWager?playerId={}'.format(self.playerId))
        assert 'parameter wager is required' in rv.data

    def test_set_wager_too_low(self):
        rv = self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, config.MIN_WAGER - 1))
        assert 'wager must be greater than' in rv.data

    def test_set_wager_too_high(self):
        rv = self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, 9999999))
        assert 'you can\'t wager more than you have' in rv.data

    def test_set_wager(self):
        rv = self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, 10))
        setWager = json.loads(rv.data)
        assert setWager['success']

        rv = self.app.get('/myTurn?playerId={}'.format(self.playerId))
        myTurn = json.loads(rv.data)
        assert myTurn['myTurn']

        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        assert player['chips'] == config.STARTING_CHIPS
        assert len(player['hand']['cards']) == 2

    def test_hit_before_wager(self):
        rv = self.app.get('/hit?playerId={}'.format(self.playerId))
        assert 'not allowed to do that right now' in rv.data

    def test_double_down_before_wager(self):
        rv = self.app.get('/doubleDown?playerId={}'.format(self.playerId))
        assert 'not allowed to do that right now' in rv.data

    def test_stand_before_wager(self):
        rv = self.app.get('/stand?playerId={}'.format(self.playerId))
        assert 'not allowed to do that right now' in rv.data

    def test_surrender_before_wager(self):
        rv = self.app.get('/surrender?playerId={}'.format(self.playerId))
        assert 'not allowed to do that right now' in rv.data


class BlackjackOnePlayerStartWithWagerTestCase(unittest.TestCase):
    name = 'max'
    wager = 10

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()
        rv = self.app.post('/player?name={}'.format(self.name))
        startInfo = json.loads(rv.data)
        self.playerId = startInfo['playerId']
        self.gameId = startInfo['game']['id']
        self.app.get('/start')
        self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))

    def tearDown(self):
        self.app.get('/reset')

    def test_get_game(self):
        rv = self.app.get('/game/{}'.format(self.gameId))
        game = json.loads(rv.data)
        assert game['id'] == self.gameId
        assert len(game['revealedCards']) == 3

    def test_set_wager_again(self):
        rv = self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))
        assert 'not allowed to do that right now' in rv.data

    def test_hit(self):
        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        assert player['chips'] == config.STARTING_CHIPS
        playerHand = player['hand']
        assert len(playerHand['cards']) == 2
        value = playerHand['value']
        rv = self.app.get('/hit?playerId={}'.format(self.playerId))
        card = json.loads(rv.data)
        value += card['value']

        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        playerHand = player['hand']
        if value <= 21:
            assert len(playerHand['cards']) == 3
        elif value > 21:
            assert len(playerHand['cards']) == 0

    def test_double_down(self):
        self.app.get('/doubleDown?playerId={}'.format(self.playerId))
        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        playerHand = player['hand']
        assert len(playerHand['cards']) == 0
        assert player['chips'] == config.STARTING_CHIPS + 2 * self.wager or player['chips'] == config.STARTING_CHIPS - 2 * self.wager

    def test_stand(self):
        self.app.get('/stand?playerId={}'.format(self.playerId))
        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        playerHand = player['hand']
        assert len(playerHand['cards']) == 0
        assert player['chips'] == config.STARTING_CHIPS + self.wager or player['chips'] == config.STARTING_CHIPS - self.wager

    def test_surrender(self):
        self.app.get('/surrender?playerId={}'.format(self.playerId))
        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        playerHand = player['hand']
        assert len(playerHand['cards']) == 0
        assert player['chips'] == config.STARTING_CHIPS - self.wager / 2


class BlackJackTwoPlayersOutOfTurnNoWagerTestCase(unittest.TestCase):
    name = 'max'
    wager = 10

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()
        self.app.post('/player?name=player')
        rv = self.app.post('/player?name={}'.format(self.name))
        startInfo = json.loads(rv.data)
        self.playerId = startInfo['playerId']
        self.gameId = startInfo['game']['id']
        self.app.get('/start')

    def tearDown(self):
        self.app.get('/reset')

    def test_set_wager(self):
        rv = self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))
        assert 'it isn\'t your turn' in rv.data

    def test_hit(self):
        rv = self.app.get('/hit?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_double_down(self):
        rv = self.app.get('/doubleDown?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_stand(self):
        rv = self.app.get('/stand?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_surrender(self):
        rv = self.app.get('/surrender?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data


class BlackJackTwoPlayersOutOfTurnWithWagerTestCase(unittest.TestCase):
    name = 'max'
    wager = 10

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()
        rv = self.app.post('/player?name=player')
        startInfo = json.loads(rv.data)
        firstPlayerId = startInfo['playerId']
        rv = self.app.post('/player?name={}'.format(self.name))
        startInfo = json.loads(rv.data)
        self.playerId = startInfo['playerId']
        self.gameId = startInfo['game']['id']
        self.app.get('/start')
        self.app.get('/setWager?playerId={}&wager={}'.format(firstPlayerId, self.wager))
        self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))

    def tearDown(self):
        self.app.get('/reset')

    def test_hit(self):
        rv = self.app.get('/hit?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_double_down(self):
        rv = self.app.get('/doubleDown?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_stand(self):
        rv = self.app.get('/stand?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data

    def test_surrender(self):
        rv = self.app.get('/surrender?playerId={}'.format(self.playerId))
        assert 'it isn\'t your turn' in rv.data


class BlackJackStartToEndTestCase(unittest.TestCase):
    name = 'max'
    wager = 10

    def setUp(self):
        application.application.config['TESTING'] = True
        self.app = application.application.test_client()
        rv = self.app.post('/player?name={}'.format(self.name))
        startInfo = json.loads(rv.data)
        self.playerId = startInfo['playerId']
        self.gameId = startInfo['game']['id']
        self.app.get('/start')

    def tearDown(self):
        self.app.get('/reset')

    def test_hit_til_bust(self):
        self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))
        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        assert player['chips'] == config.STARTING_CHIPS
        playerHand = player['hand']
        assert len(playerHand['cards']) == 2
        value = playerHand['value']
        while value <= 21:
            rv = self.app.get('/hit?playerId={}'.format(self.playerId))
            card = json.loads(rv.data)
            value += card['value']

        rv = self.app.get('/player/{}'.format(self.playerId))
        player = json.loads(rv.data)
        assert player['chips'] == config.STARTING_CHIPS - self.wager

    def test_double_after_hit(self):
        self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))
        self.app.get('/hit?playerId={}'.format(self.playerId))
        rv = self.app.get('/doubleDown?playerId={}'.format(self.playerId))
        assert 'you can\'t double down after hitting' in rv.data

    def test_surrender_after_hit(self):
        self.app.get('/setWager?playerId={}&wager={}'.format(self.playerId, self.wager))
        self.app.get('/hit?playerId={}'.format(self.playerId))
        rv = self.app.get('/surrender?playerId={}'.format(self.playerId))
        assert 'you can\'t surrender after hitting' in rv.data


if __name__ == '__main__':
    unittest.main()