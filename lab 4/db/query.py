from .row import Row

class SimpleQuery:
    def __init__(self, table):
        self.table = table
        self.selected_columns = None
        self.filter_conditions = []
        self.sort_column = None
        self.sort_ascending = True

    def select(self, columns):
        self.selected_columns = columns
        return self

    def where(self, column, operator, value):
        self.filter_conditions.append((column, operator, value))
        return self

    def order_by(self, column, ascending=True):
        self.sort_column = column
        self.sort_ascending = ascending
        return self

    def execute(self):
        results = []
        filtered = []
        for row in self.table.all_rows():
            match = True
            for col, op, val in self.filter_conditions:
                row_val = row[col]
                if op == "=" and row_val != val:
                    match = False
                    break
                elif op == ">" and not (row_val > val):
                    match = False
                    break
            if match:
                filtered.append(row)
        if self.sort_column:
            filtered.sort(key=lambda r: r[self.sort_column] if r[self.sort_column] is not None else "", reverse=not self.sort_ascending)
        for row in filtered:
            if self.selected_columns:
                results.append(Row({col: row[col] for col in self.selected_columns}))
            else:
                results.append(row)
        return results

class JoinedTable:
    def __init__(self, left_table, right_table, left_column, right_column):
        self.left_table = left_table
        self.right_table = right_table
        self.left_column = left_column
        self.right_column = right_column

    def execute(self):
        result_rows = []
        for lrow in self.left_table.all_rows():
            for rrow in self.right_table.all_rows():
                if lrow[self.left_column] == rrow[self.right_column]:
                    combined_data = {**lrow.data, **rrow.data}
                    result_rows.append(Row(combined_data))
        return result_rows
