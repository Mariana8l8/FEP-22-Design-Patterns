from .table import Table
from .column import Column
from .data_types import IntegerType, StringType, BooleanType, DateType

type_map = {
    "int": IntegerType,
    "string": StringType,
    "bool": BooleanType,
    "date": DateType
}

def create_table_with_factory(db, name, schema):
    columns = []
    for col in schema["columns"]:
        col_type = type_map[col["type"]]
        if col["type"] == "string" and "max_length" in col:
            col_instance = col_type(col["max_length"])
        else:
            col_instance = col_type()
        columns.append(Column(
            col["name"],
            col_instance,
            nullable=col.get("nullable", True),
            primary_key=col.get("primary_key", False),
            foreign_key=col.get("foreign_key")
        ))
    table = Table(name, columns)
    db.create_table(table)
    return table
