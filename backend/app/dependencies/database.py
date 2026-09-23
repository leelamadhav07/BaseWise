from typing import Optional
from app.core.config import settings
from basewise.database import Database

database = Database(settings.DATABASE_URL)

def get_database():
    if not database.is_connected():
        database.connect()

    return database

def connect_user_database(database_url: Optional[str] = None):
    global database

    target_url = database_url
    if not target_url or     target_url == "string":
        target_url = settings.DATABASE_URL

    if not target_url:
        raise ValueError("No database URL provided and default DATABASE_URL is not set.")

    # Close the existing connection
    if database.is_connected():
        database.close()

    # Use the connection string provided by the user or default settings
    database = Database(target_url)
    database.connect()

    return database