# `jeopydy`

Run a simple Jeopardy game in python. For now, this is not a package and is intended to be cloned locally to play.

I don't fully recall all the rules of Jeopardy at the moment, but some things that are not included:

* Daily double
* When a player loses control of the board who gets to pick the next category. For now mine, picks a random player leaving out the person who just answered wrong.
* Others?


## Question JSON file

First you can create a json file containing your game's questions that looks like this:

```json
{
    "Category 1": [
        {
            "Question": "This.",
            "Answer": "What is this?"
        },
        {
            "Question": "That.",
            "Answer": "What is that?"
        }
    ],
    "Category 2": [
        {
            "Question": "Foo",
            "Answer": "What is bar?"
        }
    ]
}
```

This file should be saved at the top level of the cloned directory (next to this README).

## Game Script

Then in a python script you can create your board from this json, a list of players, and a game:

```python
# imports
from jeopardy import Player, Board, Game

# create jeopardy objects
board = Board.from_json("path-to-above.json")
players = [Player("Player 1"), Player("Player 2")]
game = Game(topic="My Game's Topic", board=board, players=players)

# start the game
game.start()
```

Save this python code as a .py file. This file should be saved at the top level of the cloned directory (next to this README).

## Run Game Script

Then, from a terminal that is within this cloned directory, the game can be played with:

```
python path-to-your-game.py
```

## Sound Effects

As the host running python, it can be fun to have [this sound board](https://www.myinstants.com/en/search/?name=jeopardy) open to provide your players with sounds.
