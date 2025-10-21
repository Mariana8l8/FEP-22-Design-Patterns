from mydb.builder import TableBuilder
from mydb.types import IntegerType, StringType
from mydb.query import SimpleQuery

def test_where_comparisons_and_none(clear_database):
    db = clear_database
    t = TableBuilder("numbers").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                               .add_column("val", IntegerType(), nullable=True).build()
    db.add_table(t)
    t.insert({"val": 10}, db)
    t.insert({"val": 5}, db)
    t.insert({"val": None}, db)

    q = SimpleQuery(t)
    res_gt = q.where([("val", ">", 6)]).execute()
    assert len(res_gt) == 1 and res_gt[0]["val"] == 10

    q2 = SimpleQuery(t)
    res_null = q2.where([("val", "=", None)]).execute()
    assert isinstance(res_null, list)

def test_ordering_with_none(clear_database):
    db = clear_database
    t = TableBuilder("mix").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                           .add_column("name", StringType(), nullable=True).build()
    db.add_table(t)
    t.insert({"name": "b"}, db)
    t.insert({"name": None}, db)
    t.insert({"name": "a"}, db)
    res = SimpleQuery(t).order_by("name", ascending=True).execute()
    assert isinstance(res, list)
