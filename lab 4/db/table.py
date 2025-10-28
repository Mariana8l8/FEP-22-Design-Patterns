from .row import Row

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = {col.name: col for col in columns}
        self.rows = []
        self.next_id = 1

    def insert(self, row_data):
        for col_name, col in self.columns.items():
            value = row_data.get(col_name)
            if not col.validate(value):
                raise ValueError(f"Invalid value for column {col_name}: {value}")
        row = Row(row_data)
        row.id = self.next_id
        self.next_id += 1
        self.rows.append(row)
        return row

    def all_rows(self):
        return self.rows
