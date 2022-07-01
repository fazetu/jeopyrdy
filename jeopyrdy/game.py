from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .board import Board, Column, Tile
from .player import Player
from .utils import clear, is_int, pick1, show


@dataclass
class Game:
    topic: str
    board: Board
    players: List[Player]

    def __post_init__(self):
        i = pick1(range(len(self.players)))
        self.board_control_player = self.players[i]

    def get_player(self, name: str) -> Player:
        for player in self.players:
            if player.name == name:
                return player

        return ValueError(f"No player with that name, {name}.")

    def intro(self):
        clear()
        show("Welcome to Jeopardy!", big=True, wait=True)
        clear()

        show(f"Tonight's topic is {self.topic}", big=True, wait=True)
        clear()

        show(
            f"Our {'players are' if len(self.players) > 1 else 'player is'}",
            big=True,
            wait=True,
        )
        clear()
        for player in self.players:
            player.show_name(big=True, wait=True)
            clear()

        show(
            f"The {'categories are' if len(self.board.categories) > 1 else 'category is'}",
            big=True,
            wait=True,
        )
        clear()
        for column in self.board.columns:
            column.show_category(big=True, wait=True)
            clear()

        show("Good luck!", big=True, wait=True)

    def ask_category(self) -> str:
        category_input = input("Select a category: ")

        while True:
            if category_input == "BACK":
                return "BACK"
            elif category_input == "QUIT":
                return "QUIT"
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

    def show_category_dollar(self, category: str, dollar: int):
        show(f"{category} for ${dollar:,.0f}", big=False, wait=False)

    def ask_who_is_answering(self) -> str:
        who = input("Who? ")

        while True:
            if who == "SKIP":
                return "SKIP"
            elif who not in [player.name for player in self.players]:
                who = input("Not a player. Who? ")
            else:
                return who

    def ask_correct(self) -> bool:
        response = input("Correct? ")

        while True:
            if response == "BACK":
                return "BACK"
            elif response in ["y", "Y", "yes", "Yes", "YES"]:
                return True
            elif response in ["n", "N", "no", "No", "NO"]:
                return False
            else:
                response = input("Correct? ")

    def handle_outcome(self, name: str, correct: bool, tile: Tile):
        if name != "SKIP":
            player = self.get_player(name)

            if correct:
                player.award_money(tile.dollar)
                # board control player is the last player to answer a question correctly
                self.board_control_player = player
            else:
                player.award_money(-1 * tile.dollar)

        tile.mark_done()

    def show_player_earnings(self):
        for player in self.players:
            player.show_name_earnings(big=False, wait=False)

    def show_winner(self):
        earnings = [player.earnings for player in self.players]
        lo_to_hi = np.argsort(earnings).tolist()
        hi_to_lo = list(reversed(lo_to_hi))
        best = hi_to_lo[0]
        show(f"Congratulations {self.players[best].name}!", big=True, wait=True)

    def start(self, skip_intro: bool = False):
        if not skip_intro:
            self.intro()

        while not self.board.all_done:
            clear()

            # show the board and the player status to allow for picking of the next question
            self.show_player_earnings()
            self.board_control_player.show_my_board(big=False, wait=False)
            self.board.display()

            category = self.ask_category()
            # this probably isn't needed, just would need to go back after picking a dollar amount
            if category == "BACK":
                continue

            if category == "QUIT":
                break

            column = self.board.get_column(category)

            dollar = self.ask_dollar(column)
            # allow for repicking of category if they want
            if dollar == "BACK":
                continue

            tile = column.get_tile(int(dollar))

            # now focus on just the question that was chosen
            while True:
                clear()
                self.show_player_earnings()
                self.show_category_dollar(category, int(dollar))
                show(tile.question, big=True, wait=False)

                name = self.ask_who_is_answering()

                if name == "SKIP":
                    break

                correct = self.ask_correct()

                if correct == "BACK":
                    continue

                self.handle_outcome(name, correct, tile)

            clear()
            show(tile.question, big=False, wait=False)
            show("\n", big=False, wait=False)
            show(tile.answer, big=True, wait=True)

        # wrap up game by showing all player's earnings and congratulating winner
        clear()
        self.show_player_earnings()
        self.show_winner()
        clear()
