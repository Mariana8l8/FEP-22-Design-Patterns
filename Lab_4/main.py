from mydb.builder import TableBuilder
from mydb.database import Database
from mydb.types import IntegerType, StringType
from mydb.query import JoinedTable

db = Database()

users_table = (TableBuilder('users')
               .add_column('name', StringType(), nullable=False)
               .build())

orders_table = (TableBuilder('orders')
               .add_column('user_id', IntegerType(), nullable=False, foreign_key=('users', 'id'))
               .add_column('item', StringType(), nullable=False)
               .build())

db.add_table(users_table)
db.add_table(orders_table)

users_table.insert({"name": "Alice"}, db)
users_table.insert({"name": "Bob"}, db)
users_table.insert({"name": "Carol"}, db)

orders_table.insert({"user_id": 1, "item": "Laptop"}, db)
orders_table.insert({"user_id": 1, "item": "Mouse"}, db)
orders_table.insert({"user_id": 2, "item": "Keyboard"}, db)


join = JoinedTable(
    left_table=users_table,
    joins=[(orders_table, "id", "user_id")]
)

result = join.execute()

for row in result:
    print(row)
