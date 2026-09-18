import sys
from pathlib import Path

# Ensure backend directory is in python path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.database_service import DatabaseService
from app.core.config import settings


service = DatabaseService()

database = None

try:
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")

    database = service.connect(settings.DATABASE_URL)

    print("DatabaseService connection successful!")
    print("Connected:", database.is_connected())

finally:
    if database:
        database.close()

    print("Database connection closed.")