from .table import Table
from .column import Column

class TableBuilder:
    def __init__(self, name):
        self.name = name
        self.columns = []

    def add_column(self, name, data_type, nullable=True, primary_key=False, foreign_key=None):
        self.columns.append(Column(name, data_type, nullable, primary_key, foreign_key))
        return self

    def build(self, db=None):
        table = Table(self.name, self.columns)
        if db:
            db.create_table(table)
        return table
