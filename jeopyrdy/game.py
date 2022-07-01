from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .board import Board, Column, Tile
from .player import Player
from .utils import clear, is_int, pick1, show, wait_show


@dataclass
class Game:
    topic: str
    board: Board
    players: List[Player]

    def __post_init__(self):
        self.turn_player_i = pick1(range(len(self.players)))

    @property
    def turn_player(self) -> Player:
        return self.players[self.turn_player_i]

    def intro(self):
        clear()
        wait_show("Welcome to Jeopardy!")
        clear()

        wait_show(f"Tonight's topic is {self.topic}")
        clear()

        wait_show(f"Our {'players are' if len(self.players) > 1 else 'player is'}")
        clear()
        for name in [player.name for player in self.players]:
            wait_show(name)
            clear()

        wait_show(
            f"The {'categories are' if len(self.board.categories) > 1 else 'category is'}"
        )
        clear()
        for category in self.board.categories:
            wait_show(category)
            clear()

        wait_show("Good luck to all of our contestants!")

    def show_turn_player(self):
        print(f"It's {self.turn_player.name}'s turn")

    def ask_category(self) -> str:
        category_input = input("Select a category: ")

        while True:
            if category_input == "BACK":
                return "BACK"
            elif category_input not in self.board.categories:
                category_input = input("That is not a category. Select a category: ")
            elif category_input not in self.board.categories_playable:
                category_input = input(
                    "There are no more questions for that category. Select a category: "
                )
            else:
                return category_input

    def ask_dollar(self, column: Column) -> str:
        dollar_input = input("Choose a dollar amount: ")

        while True:
            if dollar_input == "BACK":
                return "BACK"
            elif is_int(dollar_input):
                dollar_int = int(dollar_input)

                if dollar_int not in column.dollars:
                    reason = "Not a possible dollar amount."
                elif dollar_int not in column.dollars_playable:
                    reason = "That amount has already been won."
                else:
                    return dollar_input
            else:
                reason = "Enter a number."

            dollar_input = input(f"{reason} Choose a dollar amount: ")

    def remind_category_dollar(self, category: str, dollar: int):
        print(f"{category} for ${dollar:,.0f}")

    def ask_correct(self) -> bool:
        response = input("Correct? ")

        while True:
            if response in ["y", "Y", "yes", "Yes", "YES"]:
                return True
            elif response in ["n", "N", "no", "No", "NO"]:
                return False
            else:
                response = input("Correct? ")

    def handle_correct(self, correct: bool, tile: Tile):
        if correct:
            # give turn player money
            self.turn_player.award_money(tile.dollar)

            # if correct the turn player stays the same
        else:
            # deduct turn player money
            self.turn_player.award_money(-1 * tile.dollar)

            # pick a new turn player (randomly for now) - don't know what real jeopardy does lol
            options = [i for i in range(len(self.players)) if i != self.turn_player_i]
            # only do this if there are other options for the next player
            if len(options) > 0:
                self.turn_player_i = pick1(options)

        tile.mark_done()

    def show_player_earnings(self):
        for player in self.players:
            print(f"{player.name} has ${player.earnings:,.0f}")

    def show_winner(self):
        earnings = [player.earnings for player in self.players]
        lo_to_hi = np.argsort(earnings).tolist()
        hi_to_lo = list(reversed(lo_to_hi))
        best = hi_to_lo[0]
        show(f"Congratulations {self.players[best].name}!")

    def start(self, skip_intro: bool = False):
        if not skip_intro:
            self.intro()

        while not self.board.all_done:
            clear()

            # show the board and the player status to allow for picking of the next question
            self.show_player_earnings()
            self.show_turn_player()
            self.board.display()

            category = self.ask_category()
            # this probably isn't needed, just would need to go back after picking a dollar amount
            if category == "BACK":
                continue

            column = self.board.get_column(category)

            dollar = self.ask_dollar(column)
            # allow for repicking of category if they want
            if dollar == "BACK":
                continue

            tile = column.get_tile(int(dollar))

            # now focus on just the question that was chosen
            clear()
            self.show_turn_player()
            self.remind_category_dollar(category, int(dollar))
            wait_show(tile.question)
            clear()
            self.show_turn_player()
            self.remind_category_dollar(category, int(dollar))
            show(tile.answer)
            correct = self.ask_correct()
            self.handle_correct(correct, tile)

        # wrap up game by showing all player's earnings and congratulating winner
        clear()
        self.show_player_earnings()
        self.show_winner()
