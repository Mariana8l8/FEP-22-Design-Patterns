from dataclasses import dataclass, field
from typing import Union, Optional, Any
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mydb.table import Table


@dataclass
class SimpleQuery:
    table: 'Table'
    selected_columns: Optional[list[str]] = field(default=None, init=False)
    filter_conditions: list[tuple[str, str, Union[str, int, bool, float]]] = field(default_factory=list, init=False)
    sort_column: Optional[str] = field(default=None, init=False)
    sort_ascending: bool = field(default=True, init=False)

    def __post_init__(self):
        from mydb.table import Table
        if not isinstance(self.table, Table):
            raise TypeError("Parameter 'table' must be an instance of Table")

    def select(self, columns: list[str]) -> 'SimpleQuery':
        if not isinstance(columns, list):
            raise TypeError("'columns' must be a list of column names")
        for i in columns:
            if not isinstance(i, str):
                raise TypeError("Each column name must be a string")
        self.selected_columns = columns
        return self

    def where(self, conditions: list[tuple[str, str, Union[str, int, bool, float, None]]]) -> 'SimpleQuery':
        if not isinstance(conditions, list):
            raise TypeError("'conditions' must be a list of tuples (column, operator, value)")

        for condition in conditions:
            if not isinstance(condition, tuple) or len(condition) != 3:
                raise TypeError("Each condition must be a tuple of three elements: (column, operator, value)")

            column, operator, value = condition

            if not isinstance(column, str):
                raise TypeError("The first element of each condition (column) must be a string")
            if not isinstance(operator, str):
                raise TypeError("The second element of each condition (operator) must be a string")
            if not isinstance(value, (str, int, bool, float, type(None))):
                raise TypeError("The third element of each condition (value) must be str, int, bool, float, or None")

        self.filter_conditions = conditions
        return self

    def order_by(self, column: str, ascending: bool = True) -> 'SimpleQuery':
        if not isinstance(column, str):
            raise TypeError("'column' must be a string")
        if not isinstance(ascending, bool):
            raise TypeError("'ascending' must be a boolean value")

        self.sort_column = column
        self.sort_ascending = ascending
        return self

    def execute(self) -> list[dict[str, Union[str, int, bool, float, None]]]:
        results: list[dict[str, Union[str, int, bool, float, None]]] = []

        all_rows = self.table.get_all()

        filtered_rows = []
        for row in all_rows:
            match = True
            for col, op, val in self.filter_conditions:
                row_val = row.get(col)

                if row_val is None or val is None:
                    if op == "=" and row_val is val:
                        continue
                    elif op == "!=" and row_val is not val:
                        continue
                    else:
                        match = False
                        break

                if op == "=" and row_val != val:
                    match = False
                    break
                elif op == "!=" and row_val == val:
                    match = False
                    break
                elif op == ">" and not (row_val > val):
                    match = False
                    break
                elif op == "<" and not (row_val < val):
                    match = False
                    break
                elif op == ">=" and not (row_val >= val):
                    match = False
                    break
                elif op == "<=" and not (row_val <= val):
                    match = False
                    break

            if match:
                filtered_rows.append(row)

        if self.sort_column:
            filtered_rows.sort(
                key=lambda r: r.get(self.sort_column) if r.get(self.sort_column) is not None else "",
                reverse=not self.sort_ascending
            )

        for row in filtered_rows:
            if self.selected_columns:
                row_data = {col: row[col] for col in self.selected_columns if col in row}
                results.append(row_data)
            else:
                results.append(row)

        return results

@dataclass
class JoinedTable:
    left_table: 'Table'
    joins: list[tuple['Table', str, str]] = field(default_factory=list)

    def __post_init__(self):
        from mydb.table import Table
        if not isinstance(self.left_table, Table):
            raise TypeError("left_table must be an instance of Table")
        if not isinstance(self.joins, list):
            raise TypeError("'joins' must be a list of tuples (table, column, value)")
        for j in self.joins:
            if not (isinstance(j, tuple) and len(j) == 3):
                raise TypeError("Each join must be a tuple (right_table, left_col, right_col)")
            right_table, left_col, right_col = j
            if not isinstance(right_table, Table):
                raise TypeError("right_table must be an instance of Table")
            if not isinstance(left_col, str) or not isinstance(right_col, str):
                raise TypeError("Join column names must be strings")
            if left_col not in self.left_table.columns:
                raise ValueError(f"Column '{left_col}' does not exist in left table '{self.left_table.name}'")
            if right_col not in right_table.columns:
                raise ValueError(f"Column '{right_col}' does not exist in right table '{right_table.name}'")

    def execute(self) -> list[dict[str, Any]]:
        def prefixed_row(table_name: str, row: dict[str, Any]) -> dict[str, Any]:
            return {f"{table_name}.{k}": v for k, v in row.items()}

        result_rows: list[dict[str, Any]] = [prefixed_row(self.left_table.name, r) for r in self.left_table.get_all()]

        for right_table, left_col, right_col in self.joins:
            new_result: list[dict[str, Any]] = []
            right_index: dict[Any, list[dict[str, Any]]] = {}
            for r in right_table.get_all():
                key = r.get(right_col)
                right_index.setdefault(key, []).append(prefixed_row(right_table.name, r))

            left_key_name = f"{self.left_table.name}.{left_col}"
            for left_row in result_rows:
                left_key = left_row.get(left_key_name)
                matches = right_index.get(left_key)
                if matches:
                    for right_prefixed in matches:
                        merged = {}
                        merged.update(left_row)
                        merged.update(right_prefixed)
                        new_result.append(merged)

            result_rows = new_result

        return result_rows
