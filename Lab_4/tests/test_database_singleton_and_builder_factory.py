from mydb.database import Database
from mydb.builder import TableBuilder
from mydb.types import IntegerType, StringType
import pytest

def test_database_singleton(clear_database):
    db1 = Database()
    db2 = Database()
    assert db1 is db2
    t = TableBuilder("x").add_column("id", IntegerType(), primary_key=True, nullable=False).build()
    db1.add_table(t)
    assert "x" in db2.tables

def test_tablebuilder_and_add_to_db(clear_database):
    db = clear_database
    tb = TableBuilder("tb_test").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                                .add_column("name", StringType(), nullable=False)
    table = tb.build()
    db.add_table(table)
    assert "tb_test" in db.tables
    with pytest.raises(TypeError):
        TableBuilder(123)
