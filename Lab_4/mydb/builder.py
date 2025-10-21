from dataclasses import dataclass, field
from typing import Optional

from mydb.column import Column
from mydb.table import Table
from mydb.types import DataType


@dataclass
class TableBuilder:
    name: str
    cols: list[Column] = field(default_factory=list, init=False)

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("Table name must be of type 'str'")

    def add_column(
        self,
        name: str,
        type_: DataType,
        nullable: bool = True,
        primary_key: bool = False,
        foreign_key: Optional[tuple[str, str]] = None
    ) -> "TableBuilder":
        column = Column(
            name,
            type_,
            nullable=nullable,
            primary_key=primary_key,
            foreign_key=foreign_key
        )
        self.cols.append(column)
        return self

    def build(self) -> Table:
        return Table(self.name, self.cols)
