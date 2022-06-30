from typing import List
from dataclasses import dataclass


@dataclass
class Player:
    name: str
    earnings: int = 0

    def award_money(self, amount: int):
        self.earnings += amount
