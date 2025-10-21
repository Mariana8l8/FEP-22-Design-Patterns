from dataclasses import dataclass
from datetime import date
from typing import Union


@dataclass
class Row:
    id: int
    rows: dict[str, Union[str, int, date, bool]]

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise TypeError("Row id must be an integer")
        if not isinstance(self.rows, dict):
            raise TypeError("Row rows must be a dict")

        for row_key, row_value in self.rows.items():
            if not isinstance(row_key, str):
                raise TypeError("Row key must be a string")
            if row_value is not None and not isinstance(row_value, (str, int, date, bool)):
                raise TypeError("Row value must be a str, int, date, bool or None")
