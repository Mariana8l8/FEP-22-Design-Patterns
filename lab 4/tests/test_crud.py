import pytest
from db.database import Database
from db.data_types import IntegerType, StringType
from db.builder import TableBuilder

def test_insert_and_query():
    db = Database("test_lab4")
    table = (TableBuilder("test")
             .add_column("id", IntegerType(), primary_key=True, nullable=False)
             .add_column("name", StringType(20))
             .build(db=db))
    table.insert({"id": 1, "name": "Alice"})
    table.insert({"id": 2, "name": "Bob"})
    rows = table.all_rows()
    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
