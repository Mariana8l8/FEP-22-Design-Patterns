from mydb.builder import TableBuilder
from mydb.types import IntegerType, StringType, BooleanType
import pytest

def test_insert_missing_non_nullable_raises(clear_database):
    db = clear_database
    t = TableBuilder("t1").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                          .add_column("name", StringType(), nullable=False) \
                          .build()
    db.add_table(t)
    with pytest.raises(ValueError):
        t.insert({"name": None}, db)

def test_primary_key_uniqueness(clear_database):
    db = clear_database
    t = TableBuilder("t2").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                          .add_column("code", IntegerType(), primary_key=False, nullable=False) \
                          .build()
    db.add_table(t)
    t.insert({"code": 10}, db)
    t2 = TableBuilder("t2b").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                            .add_column("code", IntegerType(), primary_key=True, nullable=False) \
                            .build()
    db.add_table(t2)
    t2.insert({"code": 1}, db)
    with pytest.raises(ValueError):
        t2.insert({"code": 1}, db)

def test_update_and_delete_behaviour(clear_database):
    db = clear_database
    t = TableBuilder("people").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                              .add_column("name", StringType(), nullable=False) \
                              .build()
    db.add_table(t)
    t.insert({"name": "A"}, db)
    t.insert({"name": "B"}, db)

    t.update(2, {"name": "B2"})
    assert any(r["id"] == 2 and r["name"] == "B2" for r in t.get_all())
    t.delete(1)
    assert all(r["id"] != 1 for r in t.get_all())
    with pytest.raises(ValueError):
        t.delete(999)
