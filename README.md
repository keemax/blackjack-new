# blackjack!

This is a blackjack server. It acts as a dealer in the form of a REST API. You are tasked with creating a program which will act as a player, consuming this API to play a set number of rounds of a simplified version of blackjack. You can create your program in any language you wish, however it is important to have python 2.7 installed, as you will want to run a local version of the blackjack dealer for testing.

To run, simply clone this repo and run `python application.py` from the root folder. If you're missing dependencies, you may install them with PIP.

you should only need flask:
Flask==0.10.1	`pip install Flask`

If you are unfamiliar with blackjack, try starting [here](http://wizardofodds.com/games/blackjack/basics/#toc-Rules)
(hint: even if you know all the rules, that website is very useful for all kinds of strategy tips)

The goal of the challenge is to create a working client that can run through several rounds against the dealer without any hiccups.
Once you have a basic client working, if time allows, try to add strategy to your player to improve its performance.

## Rules
This is a simplified version of blackjack... here are the rules
	* No splitting (this is the biggest difference from casino blackjack, I realize it hurts your odds, but it greatly simplifies the game)
	* No insurance
	* You may surrender (only on your first 2 cards)
	* Single deck
	* Dealer hits on soft 17
	* Blackjack pays out 3:2
	* Double down on any hand (only on your first 2 cards)
	* Dealer doesn't peek for blackjack



## API reference

### POST /player
##### register new player
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
    "playerId": "a7513caa-2c08-4321-bea4-6432cf30a065"
    "location": "/player/a7513caa-2c08-4321-bea4-6432cf30a065"
}
```

note: this is the only time you'll get your playerId - keep it secret, keep it safe.


### GET /players
##### get all players

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


### GET /player/<id>
##### get your player info


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
##### list all games


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


### GET /game/<id>
##### view a specific game


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
##### check whether it's your turn or not
##### parameters: playerId


`GET /myTurn?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
    "myTurn": true
}
```

### GET /setWager
##### set initial wager, must be > 5
##### parameters: playerId, wager

`GET /setWager?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf&wager=10`


```json
{
	"success": true
}
```


### GET /hit
##### adds a card to your hand
##### parameters: playerId


`GET /hit?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf


```json
{
    "value": 3,
    "suit": "hearts"
}
```


### GET /doubleDown
##### adds a card to your hand and forces you to stand. you cannot double down if you have already hit on this hand.
##### parameters: playerId


`GET /doubleDown?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf


```json
{
    "value": 3,
    "suit": "hearts"
}
```


### GET /stand
##### ends your turn
##### parameters: playerId

`GET /stand?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
	"success": true
}
```

### GET /surrender
##### forfeit half of your wager and end your turn
##### parameters: playerId

`GET /surrender?playerId=482a8c91-6999-4b99-ac4f-4260f0ee19cf`


```json
{
	"success": true
}
```

## object reference

player: player object
	chips: current chip stack. includes wager amount if a wager is currently on the table.
	name: player name, supplied by POST request to /player
	hand: hand belonging to player
		cards: list of card objects.
			value: value of a card as it applies to the point total. all face cards have value 10.
			suit: suit for funsies. you probably won't use this
		soft: whether or not this hand is "soft" aka contains an ace and has value <= 11
		value: current value of the hand. if soft, value could be this value or this value + 10
game: game object
	deckNumber: current deck being used. this value is incremented each time the deck is shuffled
	players: list of players in this game. if a player runs out of chips or takes too long, they won't be in this list.
	dealerUpCard: card object representing the dealer's face up card. this card is also included in "revealedCards".
	active: boolean representing whether or not this game is active. false before game has been started, and false after either all players run out of chips or last round has been reached.
	revealedCards: list of card objects. every time a card from the current deck is flipped face up, it will be added here (including dealerUpCard). resets when deck is shuffled.
	id: this game's ID


## General notes and errors
This may look like a REST API, but it doesn't follow many of the REST conventions. It is intended serve as a fun way to demonstrate your knowledge of consuming APIs, a very useful skill with many applications. One of the standard features of REST is a stateless server. This server is very far from stateless... it is keeping track of multiple games with multiple players, each in a certain state at any given time. Because of this, you will have to perform some non-traditional (i.e. hacky) calls to make everything work nicely. Since the server has no way of talking to the clients (to perhaps, notify a client it is his or her turn to play), you must periodically poll the server to get this information. That is the sole purpose of the `/myTurn` endpoint. Once you register your player, you must wait for the game to begin. You can do so by hitting `/game/<gameid>` every second or so (plz don't DDOS the server) until `active` is `true`. You can get info on games/players any time you want. Those endpoints shouldn't return an error unless you forget an ID or pass in an invalid one. However, all the endpoints that require `playerId` as a parameter are specific to you. You should always make sure it's your turn (by hitting `/myTurn` every second or so until `true`) before calling these. 

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

As a final note... this server is not perfect. There may or may not be ways to get unlimited money, sabotage other players, etc. If you can figure out a way to do this (excluding intentionally crashing the server), more power to you. I only ask that you first and foremost try to create a working player.

### Have fun!



