from __future__ import annotations
from typing import List
import json
from dataclasses import dataclass

import pandas as pd


@dataclass
class Tile:
    question: str
    answer: str
    dollar: int
    done: bool = False

    def mark_done(self):
        self.done = True

    def get_value(self) -> str:
        return "X" if self.done else f"{self.dollar:,.0f}"


@dataclass
class Column:
    category: str
    tiles: List[Tile]

    def __len__(self) -> int:
        return len(self.tiles)

    @property
    def all_done(self) -> bool:
        return all([tile.done for tile in self.tiles])

    @property
    def dollars(self) -> List[int]:
        return [tile.dollar for tile in self.tiles]

    @property
    def dollars_playable(self) -> List[int]:
        return [tile.dollar for tile in self.tiles if not tile.done]

    def fill_blank_tiles(self, n: int):
        have = len(self.tiles)
        if have < n:
            n_to_add = n - have
            tiles_to_add = [
                Tile(question="", answer="", dollar=0, done=True)
                for _ in range(n_to_add)
            ]
            self.tiles += tiles_to_add

    def get_tile(self, dollar: int) -> Tile:
        for tile in self.tiles:
            if dollar == tile.dollar:
                return tile

        raise ValueError(f"Cannot find tile with dollar: {dollar}")


@dataclass
class Board:
    columns: List[Column]

    def __post_init__(self):
        row_counts = [len(column) for column in self.columns]
        r = max(row_counts)

        for column in self.columns:
            column.fill_blank_tiles(r)

    @property
    def row_count(self) -> int:
        return len(self.columns[0])

    @property
    def column_count(self) -> int:
        return len(self.columns)

    @property
    def all_done(self) -> bool:
        return all([column.all_done for column in self.columns])

    @property
    def categories(self) -> List[str]:
        return [column.category for column in self.columns]

    @property
    def categories_playable(self) -> List[str]:
        return [column.category for column in self.columns if not self.all_done]

    def as_dataframe(self) -> pd.DataFrame:
        d = {}

        for column in self.columns:
            d[column.category] = [tile.get_value() for tile in column.tiles]
        
        return pd.DataFrame(d)

    def get_column(self, category: str) -> Column:
        for column in self.columns:
            if category == column.category:
                return column

        raise ValueError(f"Cannot find column with category: {category}")

    def display(self):
        print(self.as_dataframe().to_markdown(index=False, tablefmt="pretty"))

    @classmethod
    def from_json(cls, jsn: str) -> Board:
        with open(jsn, "r") as f:
            data = json.load(f)

        columns = []

        for category, questions in data.items():
            tiles = []

            for i, question in enumerate(questions):
                tile = Tile(question["Question"], question["Answer"], (i + 1) * 100)
                tiles.append(tile)

            column = Column(category, tiles)
            columns.append(column)

        return cls(columns)
