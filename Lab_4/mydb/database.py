from typing import Optional
from mydb.table import Table


class Database:
    instance: Optional['Database'] = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Database, cls).__new__(cls)
            cls.instance.tables = {}
        return cls.instance

    def add_table(self, table: 'Table') -> None:
        if not isinstance(table, Table):
            raise TypeError("table must be an instance of Table")

        if table.name in self.tables:
            raise ValueError(f"Table '{table.name}' already exists in the database")

        self.tables[table.name] = table

        for col in table.columns.values():
            if col.foreign_key is not None:
                table_name, col_name = col.foreign_key
                if table_name not in self.tables:
                    raise ValueError(f"Foreign key references non-existent table '{table_name}'")
                if col_name not in self.tables[table_name].columns:
                    raise ValueError(f"Foreign key references non-existent column '{col_name}' in table '{table_name}'")


    def get_table(self, name) -> 'Table':
        if name not in self.tables:
            raise KeyError(f"Table '{name}' does not exist")
        return self.tables[name]

    def list_tables(self) -> list[str]:
        return list(self.tables.keys())
