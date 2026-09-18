import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
from basewise.database import Database
from app.services.schema_service import SchemaService


def test_get_tables():
    db = Database()
    db.connect()
    try:
        schema = SchemaService(db)
        tables = schema.get_tables("public")
        assert isinstance(tables, list)
        assert len(tables) == 12
        assert "books" in tables
        assert "customers" in tables
        assert "orders" in tables
    finally:
        db.close()
