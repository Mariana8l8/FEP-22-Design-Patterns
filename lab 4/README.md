# Лабораторна робота №4 — Міні-СКБД

## Мета

Навчитися застосовувати ООП і патерни **Singleton**, **Builder**, **Factory Method** для створення спрощеної реляційної бази даних у пам’яті.

---

## Структура проєкту

```
lab_4/
├─ db/               # Основні класи: Database, Table, Row, Column, DataType, Builder, Factory, Query
├─ examples/         # main.py — приклад використання
└─ tests/            # Модульні тести CRUD та перевірки ключів
```

---

## Використання

### Створення бази даних

```python
from db.database import Database
db = Database("lab4_db")
```

### Builder — створення таблиці

```python
from db.builder import TableBuilder
from db.data_types import IntegerType, StringType

users = (TableBuilder("users")
         .add_column("id", IntegerType(), primary_key=True, nullable=False)
         .add_column("name", StringType(50), nullable=False)
         .build(db=db))

users.insert({"id": 1, "name": "Alice"})
```

### Factory Method — створення таблиці із схеми

```python
from db.factory import create_table_with_factory

orders_schema = {
    "columns": [
        {"name": "id", "type": "int", "nullable": False, "primary_key": True},
        {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "id")},
        {"name": "product", "type": "string", "nullable": False, "max_length": 100}
    ]
}
orders = create_table_with_factory(db, "orders", orders_schema)
orders.insert({"id": 1, "user_id": 1, "product": "Book"})
```

### Запити (SimpleQuery)

```python
from db.query import SimpleQuery

q = SimpleQuery(users).where("id", ">", 0).select(["id", "name"])
for row in q.execute():
    print(row.data)
```

### Inner Join (JoinedTable)

```python
from db.query import JoinedTable

join = JoinedTable(users, orders, "id", "user_id")
for row in join.execute():
    print(row.data)
```

### Збереження та завантаження JSON

```python
db.save_to_json("lab4_db.json")
db.load_from_json("lab4_db.json")
```

---

## Запуск прикладу

Відкрий термінал у кореневій папці `lab_4` і виконай:

```bash
python -m examples.main
```

* Створюються таблиці, вставляються рядки, робляться запити та зберігається база у JSON.
