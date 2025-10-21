from datetime import date
import pytest
from mydb.types import IntegerType, StringType, BooleanType, DateType

def test_integer_type_convert_and_validate():
    t = IntegerType()
    assert t.validate(5)
    assert t.convert("10") == 10
    assert t.convert(0) == 0
    with pytest.raises(ValueError):
        t.convert("not_int")

def test_string_type():
    t = StringType()
    assert t.validate("hello")
    assert t.convert(123) == "123"
    assert t.convert(None) is None

def test_boolean_type():
    t = BooleanType()
    assert t.convert("true") is True
    assert t.convert("0") is False
    assert t.convert(1) is True
    with pytest.raises(ValueError):
        t.convert("maybe")

def test_date_type():
    t = DateType()
    d = t.convert("2020.01.02")
    assert isinstance(d, date)
    with pytest.raises(ValueError):
        t.convert("2020-13-01")
