from typing import Optional
from app.core.config import settings
from basewise.database import Database


class DatabaseService:
    """ Handles database connection operations. """

    def connect(self, database_url: Optional[str] = None):
        """ Test and establish a database connection using the exact supplied URL. """
        url = database_url
        if url:
            url = url.strip().strip("'\"")

        if not url or url.lower() in ("", "string", "null", "none"):
            url = settings.DATABASE_URL

        database = Database(url)
        database.connect()
        return database