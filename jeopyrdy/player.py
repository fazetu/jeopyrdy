from typing import Optional
from dataclasses import dataclass

from .utils import show


@dataclass
class Player:
    name: str
    earnings: int = 0

    def award_money(self, amount: int):
        self.earnings += amount

    def show_name(self, big: bool, wait: bool) -> Optional[str]:
        return show(self.name, big, wait)

    def show_name_earnings(self, big: bool, wait: bool) -> Optional[str]:
        return show(f"{self.name} has ${self.earnings:,.0f}", big, wait)

    def show_my_board(self, big: bool, wait: bool) -> Optional[str]:
        return show(f"{self.name}'s board", big, wait)
