# examples/main.py
from db.database import Database
from db.builder import TableBuilder
from db.factory import create_table_with_factory
from db.data_types import IntegerType, StringType
from db.query import SimpleQuery, JoinedTable

# --- Створюємо базу ---
db = Database("lab4_db")

# --- Таблиця users через Builder ---
users = (TableBuilder("users")
         .add_column("id", IntegerType(), primary_key=True, nullable=False)
         .add_column("name", StringType(50), nullable=False)
         .build(db=db))
users.insert({"id": 1, "name": "Alice"})
users.insert({"id": 2, "name": "Bob"})

# --- Таблиця orders через Factory ---
orders_schema = {
    "columns": [
        {"name": "id", "type": "int", "nullable": False, "primary_key": True},
        {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "id")},
        {"name": "product", "type": "string", "nullable": False, "max_length": 100}
    ]
}
orders = create_table_with_factory(db, "orders", orders_schema)
orders.insert({"id": 1, "user_id": 1, "product": "Book"})
orders.insert({"id": 2, "user_id": 2, "product": "Laptop"})

# --- SimpleQuery ---
q = SimpleQuery(users).select(["id", "name"])
for row in q.execute():
    print(row.data)

# --- JOIN ---
join = JoinedTable(users, orders, "id", "user_id")
for row in join.execute():
    print(row.data)

# --- Збереження в JSON ---
db.save_to_json("lab4_db.json")