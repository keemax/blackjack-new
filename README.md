# blackjack!

This is a blackjack server. It acts as a dealer in the form of a REST API. You are tasked with creating a program which will act as a player, consuming this API to play a set number of rounds of a simplified version of blackjack. You can create your program in any language you wish, however it is important to have python 2.7 installed, as you will want to run a local version of the blackjack dealer for testing.

To run, simply clone this repo and run `python application.py` from the root folder. If you're missing dependencies, you may install them with PIP.

you should only need flask:  
Flask==0.10.1	`pip install Flask`

if you don't have pip, install it via
`wget https://bootstrap.pypa.io/get-pip.py`
`python get-pip.py`

If you are unfamiliar with blackjack, try starting [here](http://wizardofodds.com/games/blackjack/basics/#toc-Rules)  
(hint: even if you know all the rules, that website is very useful for all kinds of strategy tips)

The goal of the challenge is to create a working client that can run through several rounds against the dealer without any hiccups.
Once you have a basic client working, if time allows, try to add strategy to your player to improve its performance.

## Rules
This is a simplified version of blackjack... here are the rules:
* No splitting (this is the biggest difference from casino blackjack, I realize it hurts your odds, but it greatly simplifies the game)
* No insurance
* You may surrender (only on your first 2 cards)
* Single deck
* Dealer hits on soft 17
* Blackjack pays out 3:2
* Double down on any hand (only on your first 2 cards)
* Dealer doesn't peek for blackjack



## API Reference

### POST /player
##### Register new player with provided name. Gives you 1000 chips to start and assigns you to a game.
##### parameters: `name`


`POST /player?name=max`


```json
{
    "player": {
        "chips": 1000,
        "name": "max",
        "hand": {
            "cards": [],
            "soft": false,
            "value": 0
        }
    },
    "game": {
        "deckNumber": 0,
        "players": [
            {
                "chips": 1000,
                "name": "max",
                "hand": {
                    "cards": [],
                    "soft": false,
                    "value": 0
                }
            }
        ],
        "dealerUpCard": null,
        "active": false,
        "revealedCards": [],
        "id": "d701094d-2824-4b8f-87a5-039cca330488"
    },
    "playerId": "a7513caa-2c08-4321-bea4-6432cf30a065",
    "location": "/player/a7513caa-2c08-4321-bea4-6432cf30a065"
}
```

Note: Rhis is the only time you'll get your playerId - keep it secret, keep it safe.


### GET /players
##### Get all players.

`GET /players`


```json
[
    {
        "chips": 1050,
        "name": "sarah",
        "hand": {
            "cards": [],
            "soft": false,
            "value": 0
        }
    },
    {
        "chips": 995,
        "name": "max",
        "hand": {
            "cards": [],
            "soft": false,
            "value": 0
        }
    }
]
```


### GET /player/:id
##### Get your player info.


`GET /player/482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
    "chips": 715,
    "name": "sarah",
    "hand": {
        "cards": [
            {
                "value": 9,
                "suit": "hearts"
            },
            {
                "value": 3,
                "suit": "hearts"
            }
        ],
        "soft": false,
        "value": 12
    }
}
```


### GET /games
##### List all games.


`GET /games`


```json
[
    {
        "deckNumber": 2,
        "players": [
            {
                "chips": 980,
                "name": "max",
                "hand": {
                    "cards": [
                        {
                            "value": 10,
                            "suit": "diamonds"
                        },
                        {
                            "value": 2,
                            "suit": "clubs"
                        },
                        {
                            "value": 10,
                            "suit": "hearts"
                        }
                    ],
                    "soft": false,
                    "value": 22
                }
            },
            {
                "chips": 1035,
                "name": "bob",
                "hand": {
                    "cards": [
                        {
                            "value": 7,
                            "suit": "spades"
                        },
                        {
                            "value": 10,
                            "suit": "clubs"
                        }
                    ],
                    "soft": false,
                    "value": 17
                }
            },
            {
                "chips": 1070,
                "name": "sarah",
                "hand": {
                    "cards": [
                        {
                            "value": 10,
                            "suit": "diamonds"
                        },
                        {
                            "value": 10,
                            "suit": "diamonds"
                        }
                    ],
                    "soft": false,
                    "value": 20
                }
            }
        ],
        "dealerUpCard": {
            "value": 3,
            "suit": "hearts"
        },
        "active": true,
        "revealedCards": [
            {
                "value": 5,
                "suit": "clubs"
            },
            {
                "value": 1,
                "suit": "hearts"
            },
            {
                "value": 8,
                "suit": "hearts"
            },
            {
                "value": 2,
                "suit": "spades"
            },
            {
                "value": 10,
                "suit": "clubs"
            },
            {
                "value": 2,
                "suit": "clubs"
            },
            {
                "value": 10,
                "suit": "clubs"
            },
            {
                "value": 10,
                "suit": "diamonds"
            },
            {
                "value": 3,
                "suit": "hearts"
            },
            {
                "value": 10,
                "suit": "hearts"
            }
        ],
        "id": "25104811-064d-4331-8b0c-8fe114386918"
    }
]
```


### GET /game/:id
##### View a specific game.


`GET /game/25104811-064d-4331-8b0c-8fe114386918`


```json
{
    "deckNumber": 2,
    "players": [
        {
            "chips": 980,
            "name": "max",
            "hand": {
                "cards": [
                    {
                        "value": 10,
                        "suit": "diamonds"
                    },
                    {
                        "value": 2,
                        "suit": "clubs"
                    },
                    {
                        "value": 10,
                        "suit": "hearts"
                    }
                ],
                "soft": false,
                "value": 22
            }
        },
        {
            "chips": 1035,
            "name": "bob",
            "hand": {
                "cards": [
                    {
                        "value": 7,
                        "suit": "spades"
                    },
                    {
                        "value": 10,
                        "suit": "clubs"
                    }
                ],
                "soft": false,
                "value": 17
            }
        },
        {
            "chips": 1070,
            "name": "sarah",
            "hand": {
                "cards": [
                    {
                        "value": 10,
                        "suit": "diamonds"
                    },
                    {
                        "value": 10,
                        "suit": "diamonds"
                    }
                ],
                "soft": false,
                "value": 20
            }
        }
    ],
    "dealerUpCard": {
        "value": 3,
        "suit": "hearts"
    },
    "active": true,
    "revealedCards": [
        {
            "value": 5,
            "suit": "clubs"
        },
        {
            "value": 1,
            "suit": "hearts"
        },
        {
            "value": 8,
            "suit": "hearts"
        },
        {
            "value": 2,
            "suit": "spades"
        },
        {
            "value": 10,
            "suit": "clubs"
        },
        {
            "value": 10,
            "suit": "spades"
        },
        {
            "value": 8,
            "suit": "clubs"
        },
        {
            "value": 5,
            "suit": "hearts"
        },
        {
            "value": 10,
            "suit": "hearts"
        },
        {
            "value": 1,
            "suit": "spades"
        },
        {
            "value": 9,
            "suit": "diamonds"
        },
        {
            "value": 10,
            "suit": "diamonds"
        },
        {
            "value": 7,
            "suit": "spades"
        },
        {
            "value": 10,
            "suit": "diamonds"
        },
        {
            "value": 2,
            "suit": "clubs"
        },
        {
            "value": 10,
            "suit": "clubs"
        },
        {
            "value": 10,
            "suit": "diamonds"
        },
        {
            "value": 3,
            "suit": "hearts"
        },
        {
            "value": 10,
            "suit": "hearts"
        }
    ],
    "id": "25104811-064d-4331-8b0c-8fe114386918"
}
```


### GET /myTurn
##### Check whether it's your turn or not.
##### parameters: playerId


`GET /myTurn?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
    "myTurn": true
}
```

### GET /setWager
##### Set initial wager, must be >= 5. Tt must be your turn to call this.
##### parameters: playerId, wager

`GET /setWager?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf&wager=10`


```json
{
	"success": true
}
```


### GET /hit
##### Adds a card to your hand. It must be your turn to call this. If your resulting hand is > 21, your turn is over, otherwise, you may hit again or stand.
##### parameters: playerId


`GET /hit?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
    "value": 3,
    "suit": "hearts"
}
```


### GET /doubleDown
##### Adds a card to your hand and forces you to stand. It must be your turn to call this. You cannot double down if you have already hit on this hand.
##### parameters: playerId


`GET /doubleDown?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
    "value": 3,
    "suit": "hearts"
}
```


### GET /stand
##### Ends your turn. It must be your turn to call this.
##### parameters: playerId

`GET /stand?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
	"success": true
}
```

### GET /surrender
##### Forfeit half of your wager and end your turn. It must be your turn to call this.
##### parameters: playerId

`GET /surrender?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
	"success": true
}
```

## Object Reference

**player:** player object  
  -**chips:** Current chip stack. Includes wager amount if a wager is currently on the table.  
  -**name:** Player name, supplied by POST request to `/player`.  
  -**hand:** Hand belonging to player.  
    --**cards:** List of card objects.  
      ---**value:** Value of a card as it applies to the point total. All face cards have value 10.  
      ---**suit:** Suit for funsies. You probably won't use this  
    --**soft:** Whether or not this hand is "soft" aka contains an ace and has value <= 11.  
    --**value:** Current value of the hand. If soft, value could be this value or this value + 10.  
**game:** Game object.  
  -**deckNumber:** Current deck being used. This value is incremented each time the deck is shuffled.  
  -**players:** List of players in this game. If a player runs out of chips or takes too long, they won't be in this list.  
  -**dealerUpCard:** Card object representing the dealer's face up card. This card is also included in "revealedCards".  
  -**active:** Boolean representing whether or not this game is active. False before game has been started, and false after either all players run out of chips or last round has been reached.  
  -**revealedCards:** List of card objects. Every time a card from the current deck is flipped face up, it will be added here (including dealerUpCard). Resets when deck is shuffled.  
  -**id:** this game's ID.  



## General Notes and Errors
This may look like a REST API, but it doesn't follow many of the REST conventions. It is intended serve as a fun way to demonstrate your knowledge of consuming APIs, a very useful skill with many applications. One of the standard features of REST is a stateless server. This server is very far from stateless... it is keeping track of multiple games with multiple players, each in a certain state at any given time. Because of this, you will have to perform some non-traditional (i.e. hacky) calls to make everything work nicely. Since the server has no way of talking to the clients (to perhaps, notify a client it is his or her turn to play), you must periodically poll the server to get this information. That is the sole purpose of the `/myTurn` endpoint. You can get info on games/players any time you want. Those endpoints shouldn't return an error unless you forget an ID or pass in an invalid one. However, all the endpoints that require `playerId` as a parameter are specific to you. You should always make sure it's your turn (by hitting `/myTurn` until `true`) before calling these. Please insert a short sleep (~1 second) between consecutive calls to `/myTurn`, or else the game will turn into a coordinated DDOS attack.

Here's some example errors:

##### calling `/hit` out of turn:

```json
{
	"error": "it isn't your turn!"
}
```

##### calling `/hit` before calling `/setWager` after a new deal

```json
{
	"error": "you're not allowed to do that right now"
}
```

##### calling `/doubleDown` after hitting on the same hand

```json
{
	"error": "you can't double down after hitting"
}
```





## A quick run-through in python using the requests module

Let's start off by registering a player
```python
>>> resp = requests.post('http://localhost:5000/player?name=max')
>>> resp.json()
{u'playerId': u'99de72bf-85e4-42c3-ba10-59e8f27b93b8', u'player': {u'chips': 1000, u'name': u'max', u'hand': {u'cards': [], u'soft': False, u'value': 0}}, u'game': {u'deckNumber': 0, u'players': [{u'chips': 1000, u'name': u'max', u'hand': {u'cards': [], u'soft': False, u'value': 0}}], u'dealerUpCard': None, u'active': False, u'revealedCards': [], u'id': u'cb77cd36-18f0-4793-81fa-4761adbac5a7'}, u'location': u'/player/99de72bf-85e4-42c3-ba10-59e8f27b93b8'}
>>> startInfo = resp.json()
>>> playerId = startInfo['playerId']
>>> playerId
u'99de72bf-85e4-42c3-ba10-59e8f27b93b8'
```
Cool... my player is registered, and I have a playerId for future requests.

If you're testing your player locally, you'll have to start the game yourself. If we're all playing on the global server, I'll start it when everyone is ready.

```python
>>> requests.get('http://localhost:5000/start')
```

Since this game only has one non-dealer player, we know it's our turn right now. Just to be safe, let's check.

```python
>>> while not requests.get('http://localhost:5000/myTurn?playerId={}}'.format(playerId)).json()['myTurn']:
...     time.sleep(1)
... 
>>> 
```

Alright, it's our turn. Let's put a wager on the table. How about 20 chips.

```python
>>> requests.get('http://localhost:5000/setWager?playerId={}&wager={}'.format(playerId, 20))
<Response [200]>
>>> 
```

Before we check to see what was dealt, let's wait until it's our turn again. If other players take a second to set their wagers, the cards may not have been dealt yet.

```python
>>> while not requests.get('http://localhost:5000/myTurn?playerId={}}'.format(playerId)).json()['myTurn']:
...     time.sleep(1)
... 
>>> 
```

Alright, let's check out our hand

```python
>>> resp = requests.get('http://localhost:5000/player/{}'.format(playerId))
>>> player = resp.json()
>>> player['hand']
{u'cards': [{u'value': 8, u'suit': u'spades'}, {u'value': 6, u'suit': u'clubs'}], u'soft': False, u'value': 14}
```

Hmm... a 14. Not the best. Let's check the dealer up card so we make a more informed decision.

```python
>>> resp = requests.get('http://localhost:5000/game/b456c26d-e379-4348-90b2-8cd125579d6c')
>>> game = resp.json()
>>> game['dealerUpCard']
{u'value': 6, u'suit': u'hearts'}
```

Well the dealer is showing a 6, so I think we should stay on this one and hope they bust.

```python
>>> requests.get('http://localhost:5000/stand?playerId=60c1f83c-f245-47b2-9db6-1d7f11994403')
<Response [200]>
```

Alright, let's see what happened.

```python
>>> resp = requests.get('http://localhost:5000/player/60c1f83c-f245-47b2-9db6-1d7f11994403')
>>> player = resp.json()
>>> player['chips']
980
```

Bummer, we lost :(

We can check the revealed cards for this deck to see how the round ended

```python
>>> resp = requests.get('http://localhost:5000/game/b456c26d-e379-4348-90b2-8cd125579d6c')
>>> game = resp.json()
>>> game['revealedCards']
[{u'value': 8, u'suit': u'spades'}, {u'value': 6, u'suit': u'clubs'}, {u'value': 6, u'suit': u'hearts'}, {u'value': 9, u'suit': u'diamonds'}, {u'value': 4, u'suit': u'spades'}]
```

Looks like the dealer drew a 9 and then a 4, for a total 19. Rats!



## Final Thoughts

If we have time, we can play games with multiple players and see who ends up with the most chips (or lasts the longest before losing). The server has a built in monitor that will kick players who haven't done anything in 10 seconds, so make sure your player can last by itself before joining.  

As a final note... this server is not perfect. It was hastily written by one developer who may or may not have been hungover for part of the time. There may or may not be ways to get unlimited money, sabotage other players, etc. If you can figure out a way to do this (excluding intentionally crashing the server), more power to you. I only ask that you first and foremost create a working player with a solid strategy, as that is the surest way to win.

As far as blackjack strategy goes, the internet is your oyster. If there's something missing in the endpoints described above that you need to make your strategy better, ask me and I'll try to add it on the fly.

### Have fun!

## global server
http://ec2-52-25-237-207.us-west-2.compute.amazonaws.com



