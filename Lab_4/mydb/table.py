from dataclasses import dataclass, field
from datetime import date
from typing import Union

from mydb.query import SimpleQuery
from mydb.types import IntegerType
from mydb.column import Column
from mydb.row import Row
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mydb.database import Database


@dataclass
class Table:
    name: str
    columns: list['Column']
    rows: list['Row'] = field(default_factory=list, init=False)
    next_id: int = field(default=1, init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("Table name must be a string")

        if not isinstance(self.columns, list):
            raise TypeError("columns must be a list[Column]")
        for col in self.columns:
            if not isinstance(col, Column):
                raise TypeError("All elements in columns must be instances of Column")

        names = [col.name for col in self.columns]
        if len(names) != len(set(names)):
            raise ValueError("Column names must be unique")

        columns: list[Column] = [col for col in self.columns if col.name != "id"]
        id_column = Column("id", IntegerType(), primary_key=True, nullable=False)
        columns.insert(0, id_column)

        self.columns: dict[str, Column] = {col.name: col for col in columns}

    def insert(self, row: dict[str, Union[str, int, date, bool, None]], database: 'Database') -> None:
        if not isinstance(row, dict):
            raise TypeError("Row to insert must be a dict")

        row.pop('id', None)

        for col_name, col in self.columns.items():
            if col_name == "id":
                continue

            value = row.get(col_name, None)

            if value is None:
                if not col.nullable or col.primary_key:
                    raise ValueError(f"Column '{col_name}' cannot be null")
                continue

            value = col.type.convert(value)
            if not col.type.validate(value):
                raise ValueError(
                    f"Invalid value for column '{col_name}': "
                    f"expected type '{col.type.__class__.__name__}', got '{type(value).__name__}'"
                )

            if col.primary_key:
                for r in self.rows:
                    if r.rows[col_name] == value:
                        raise ValueError(f"Duplicate value for primary key column '{col_name}': {value}")

            if col.foreign_key is not None:
                fk_table_name, fk_col_name = col.foreign_key
                fk_table = database.get_table(fk_table_name)
                fk_values = [
                    r.id if fk_col_name == "id" else r.rows.get(fk_col_name)
                    for r in fk_table.rows
                ]
                if value not in fk_values:
                    raise ValueError(
                        f"Foreign key violation: value '{value}' not found in '{fk_table_name}.{fk_col_name}'"
                    )

            row[col_name] = value

        self.rows.append(Row(self.next_id, row))
        self.next_id += 1

    def get_all(self) -> list[dict[str, Union[str, int, date, bool, None]]]:
        out: list[dict[str, Union[str, int, date, bool, None]]] = []

        for row in self.rows:
            item: dict[str, Union[str, int, date, bool, None]] = {"id": row.id}
            for colm_name in self.columns.keys():
                if colm_name != "id":
                    item[colm_name] = row.rows.get(colm_name)
            out.append(item)
        return out

    def update(self, id: int, row: dict[str, Union[str, int, date, bool, None]]) -> None:
        target_row = next((r for r in self.rows if r.id == id), None)
        if target_row is None:
            raise ValueError(f"No row found with id={id}")

        for col_name, value in row.items():
            if col_name == "id":
                continue
            if col_name not in self.columns:
                raise KeyError(f"Unknown column '{col_name}'")
            col = self.columns[col_name]
            if value is None and not col.nullable:
                raise ValueError(f"Column '{col_name}' cannot be null")
            if value is not None and not col.type.validate(value):
                value = col.type.convert(value)
            target_row.rows[col_name] = value

    def delete(self, id: int) -> None:
        target_row = next((r for r in self.rows if r.id == id), None)
        if target_row is None:
            raise ValueError(f"No row found with id={id}")

        self.rows.remove(target_row)

    def filter(self, conditions: list[tuple[str, str, Union[str, int, bool, float]]]) -> list[dict]:
        return SimpleQuery(self).where(conditions).execute()

    def sort(self, column: str, ascending: bool = True) -> list[dict]:
        return SimpleQuery(self).order_by(column, ascending).execute()

    def select(self, columns: list[str]) -> list[dict]:
        return SimpleQuery(self).select(columns).execute()
