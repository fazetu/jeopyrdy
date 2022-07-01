# `jeopyrdy`

Pronounced like "Jeopardy".

Run a simple Jeopardy game in python. For now, this is not a package and is intended to be cloned locally to play.

Rules of Jeopardy that are not implemented:

* Daily double.
* No final Jeopardy.
* Others?

## Install Dependencies

The code in this repository relies on a few non-standard library packages. They can be installed from a terminal that is within this cloned directory with:

```
python -m pip install -r requirements.txt
```

## Question CSV file

First you can create a csv file containing your game's questions that looks like this:

```
Category,Question,Answer
Category 1,This.,What is this?
Category 1,That.,What is that?
Category 2,Foo.,What is bar?
```

This file should be saved at the top level of the cloned directory (next to this README).

## Game Script

Then in a python script you can create your board from this csv, a list of players, and a game:

```python
# imports
from jeopardy import Player, Board, Game

# create jeopardy objects
board = Board.from_file("path-to-above.csv")
players = [Player("Player 1"), Player("Player 2")]
game = Game(topic="My Game's Topic", board=board, players=players)

# start the game
game.start()
```

Save this python code as a .py file. This file should be saved at the top level of the cloned directory (next to this README).

## Run Game Script

Then, from a terminal that is within this cloned directory, and from a python environment with the dependencies installed, the game can be played with:

```
python path-to-your-game.py
```

## Sound Effects

As the host running python, it can be fun to have [this sound board](https://www.myinstants.com/en/search/?name=jeopardy) open to provide your players with sounds.
