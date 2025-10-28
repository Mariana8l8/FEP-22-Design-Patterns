from .table import Table
from .column import Column
from .row import Row
import json

class Database:
    _instance = None

    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.name = name
            cls._instance.tables = {}
        return cls._instance

    def create_table(self, table):
        for col in table.columns.values():
            if col.foreign_key:
                fk_table_name, fk_col_name = col.foreign_key
                if fk_table_name not in self.tables or fk_col_name not in self.tables[fk_table_name].columns:
                    raise ValueError(f"Invalid foreign key {col.foreign_key}")
        self.tables[table.name] = table

    def get_table(self, name):
        return self.tables.get(name)

    # JSON-збереження/завантаження
    def save_to_json(self, filename):
        db_data = {}
        for table_name, table in self.tables.items():
            db_data[table_name] = {
                "columns": [
                    {
                        "name": col.name,
                        "type": col.data_type.__class__.__name__,
                        "nullable": col.nullable,
                        "primary_key": col.primary_key,
                        "foreign_key": col.foreign_key
                    } for col in table.columns.values()
                ],
                "rows": [row.data for row in table.rows]
            }
        with open(filename, "w") as f:
            json.dump(db_data, f, indent=4)
        print(f"Database saved to {filename}")

    def load_from_json(self, filename):
        with open(filename, "r") as f:
            db_data = json.load(f)
        self.tables = {}
        from .data_types import IntegerType, StringType, BooleanType, DateType
        type_map = {
            "IntegerType": IntegerType,
            "StringType": StringType,
            "BooleanType": BooleanType,
            "DateType": DateType
        }
        for table_name, table_info in db_data.items():
            columns = []
            for col in table_info["columns"]:
                dtype_class = type_map.get(col["type"], StringType)
                if col["type"] == "StringType":
                    col_instance = dtype_class(50)
                else:
                    col_instance = dtype_class()
                columns.append(Column(
                    col["name"],
                    col_instance,
                    nullable=col["nullable"],
                    primary_key=col["primary_key"],
                    foreign_key=col["foreign_key"]
                ))
            table = Table(table_name, columns)
            for row_data in table_info["rows"]:
                table.insert(row_data)
            self.tables[table_name] = table
        print(f"Database loaded from {filename}")
