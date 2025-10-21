from dataclasses import dataclass
from typing import Optional
from mydb.types import DataType


@dataclass
class Column:
    name: str
    type: 'DataType'
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[tuple[str, str]] = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("Column name must be a string")
        if not isinstance(self.type, DataType):
            raise TypeError("Column type must be a data type")
        if not isinstance(self.nullable, bool):
            raise TypeError("Column nullable must be a boolean")
        if not isinstance(self.primary_key, bool):
            raise TypeError("Column primary_key must be a boolean")
        if self.foreign_key is not None:
            if not (isinstance(self.foreign_key, tuple) and len(self.foreign_key) == 2) and isinstance(self.foreign_key[0], str) and isinstance(self.foreign_key[1], str):
                raise TypeError("foreign_key must be a tuple (table_name, column_name)")
