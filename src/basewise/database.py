import os
import psycopg2
from dotenv import load_dotenv

# Automatically load environment variables from .env or backend/.env if present
load_dotenv()
backend_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend", ".env")
if os.path.exists(backend_env):
    load_dotenv(backend_env)



class DatabaseError(Exception):
    """Base exception for database operations."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when connecting to the database fails."""

    pass


class DatabaseAuthenticationError(DatabaseConnectionError):
    """Raised when database authentication fails."""

    pass


class DatabaseTimeoutError(DatabaseConnectionError):
    """Raised when database connection times out or network is unreachable."""

    pass


class Database:
    """Handles the PostgreSQL database connection."""

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.connection = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        if not self.database_url:
            raise DatabaseConnectionError(
                "Database URL is not specified and DATABASE_URL environment variable is not set."
            )

        try:
            self.connection = psycopg2.connect(self.database_url)
            return self.connection
        except psycopg2.OperationalError as e:
            err_msg = str(e)
            err_msg_lower = err_msg.lower()

            if (
                "password authentication failed" in err_msg_lower
                or "tenant/user" in err_msg_lower
                or "authentication failed" in err_msg_lower
            ):
                raise DatabaseAuthenticationError(
                    f"Authentication failed: {err_msg.strip()}"
                ) from e
            elif (
                "timeout" in err_msg_lower
                or "timed out" in err_msg_lower
                or "unreachable" in err_msg_lower
                or "could not translate host name" in err_msg_lower
                or "connection refused" in err_msg_lower
                or "0x0000274c" in err_msg_lower
            ):
                raise DatabaseTimeoutError(
                    f"Connection timed out or network unreachable: {err_msg.strip()}"
                ) from e
            else:
                raise DatabaseConnectionError(
                    f"Database connection failed: {err_msg.strip()}"
                ) from e
        except Exception as e:
            raise DatabaseConnectionError(
                f"Unexpected connection error: {e}"
            ) from e

    def close(self):
        """Close the database connection."""
        if self.connection:
            try:
                self.connection.close()
            finally:
                self.connection = None

    def is_connected(self):
        """Check whether the database connection is active."""
        if self.connection is None:
            return False
        try:
            return self.connection.closed == 0
        except Exception:
            return False