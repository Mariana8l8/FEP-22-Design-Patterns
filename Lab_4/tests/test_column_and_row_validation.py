import pytest
from datetime import date
from mydb.column import Column
from mydb.types import StringType
from mydb.row import Row

def test_column_basic():
    c = Column("name", StringType(), nullable=False)
    assert c.name == "name"
    assert c.nullable is False

def test_row_validation_accepts_none_and_types():
    r = Row(1, {"name": "Alice", "age": 30, "flag": True, "dob": date(2000,1,1)})
    assert r.id == 1

def test_row_rejects_bad_key_or_type():
    with pytest.raises(TypeError):
        Row("not_int", {"a": 1})
    with pytest.raises(TypeError):
        Row(1, {"not_key_type": 1, 2: "bad"})
