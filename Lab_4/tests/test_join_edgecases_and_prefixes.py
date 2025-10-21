from mydb.builder import TableBuilder
from mydb.types import IntegerType, StringType
from mydb.query import JoinedTable

def test_join_no_matches_returns_empty(clear_database):
    db = clear_database
    users = TableBuilder("u").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                             .add_column("name", StringType()).build()
    db.add_table(users)
    orders = TableBuilder("o").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                              .add_column("user_id", IntegerType(), foreign_key=('u', 'id')).build()
    db.add_table(orders)
    users.insert({"name": "X"}, db)
    jt = JoinedTable(left_table=users, joins=[(orders, "id", "user_id")])
    res = jt.execute()
    assert res == []

def test_join_prefixes_and_values(clear_database):
    db = clear_database
    users = TableBuilder("users").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                                .add_column("name", StringType()).build()
    db.add_table(users)
    orders = TableBuilder("orders").add_column("id", IntegerType(), primary_key=True, nullable=False) \
                                  .add_column("user_id", IntegerType(), foreign_key=('users', 'id')).add_column("product", StringType()).build()
    db.add_table(orders)
    users.insert({"name": "A"}, db)
    orders.insert({"user_id": 1, "product": "p1"}, db)
    res = JoinedTable(left_table=users, joins=[(orders, "id", "user_id")]).execute()
    assert res and "users.id" in res[0] and "orders.product" in res[0]
    assert res[0]["users.id"] == res[0]["orders.user_id"]
