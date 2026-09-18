import sys
from pathlib import Path

# Add backend directory to sys.path dynamically for robust cross-platform imports
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from basewise.database import Database
from app.services.schema_service import SchemaService


db = Database()

try:
    db.connect()

    schema = SchemaService(db)

    tables = schema.get_tables()

    print("Tables found:")
    
    for table in tables:
        print("-", table)

finally:
    db.close()