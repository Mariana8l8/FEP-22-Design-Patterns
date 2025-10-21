import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from mydb.database import Database

@pytest.fixture(autouse=True)
def clear_database():
    Database._instance = None
    db = Database()
    if hasattr(db, "tables"):
        db.tables.clear()
    yield db
    if hasattr(db, "tables"):
        db.tables.clear()
