from app.core.config import settings
from basewise.database import Database

database = Database(settings.DATABASE_URL)

def get_database():
    if not database.is_connected():
        database.connect()
    return database