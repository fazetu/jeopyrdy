from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Optional

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
        return pd.DataFrame(
            {
                column.category: [tile.get_value() for tile in column.tiles]
                for column in self.columns
            }
        )

    def get_column(self, category: str) -> Column:
        for column in self.columns:
            if category == column.category:
                return column

        raise ValueError(f"Cannot find column with category: {category}")

    def display(self):
        print(self.as_dataframe().to_markdown(index=False, tablefmt="pretty"))

    @classmethod
    def from_json(
        cls, jsn: str, max_questions_per_category: Optional[int] = None
    ) -> Board:
        with open(jsn, "r") as f:
            data = json.load(f)

        columns = []

        for category, questions in data.items():
            tiles = []

            for i, question in enumerate(questions):
                if "Question" not in question.keys():
                    raise KeyError(
                        f"'Question' is not a key in {category}'s element {i}"
                    )

                if "Answer" not in question.keys():
                    raise KeyError(
                        f"'Answer' is not a key in {category}'s element {i}"
                    )

                tile = Tile(
                    question=question["Question"],
                    answer=question["Answer"],
                    dollar=(i + 1) * 100,
                    done=False,
                )

                tiles.append(tile)

            if max_questions_per_category is not None:
                # slicing like this can go beyond the length of tiles and not bomb
                tiles = tiles[:max_questions_per_category]

            column = Column(category=category, tiles=tiles)
            columns.append(column)

        return cls(columns=columns)

    @classmethod
    def from_csv(
        cls, csv: str, max_questions_per_category: Optional[int] = None
    ) -> Board:
        questions = pd.read_csv(csv)
        cols = questions.columns.tolist()

        if "Category" not in cols:
            raise KeyError("'Category' is not a column in your csv")

        if "Question" not in cols:
            raise KeyError("'Question' is not a column in your csv")

        if "Answer" not in cols:
            raise KeyError("'Answer' is not a column in your csv")

        if max_questions_per_category is not None:
            questions = questions.groupby("Category").head(
                max_questions_per_category
            )

        columns = []

        for category, df in questions.groupby("Category"):
            tiles = []

            for i, tpl in enumerate(df.itertuples(index=False)):
                tile = Tile(
                    question=tpl.Question,
                    answer=tpl.Answer,
                    dollar=(i + 1) * 100,
                    done=False,
                )
                tiles.append(tile)

            column = Column(category=category, tiles=tiles)
            columns.append(column)

        return cls(columns=columns)
