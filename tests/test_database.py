import pytest
from basewise.database import (
    Database,
    DatabaseError,
    DatabaseConnectionError,
    DatabaseAuthenticationError,
    DatabaseTimeoutError,
)


def test_database_connection_success():
    db = Database()
    conn = db.connect()
    assert conn is not None
    assert db.is_connected() is True
    db.close()
    assert db.is_connected() is False


def test_database_missing_url_raises():
    db = Database(database_url="")
    db.database_url = None
    with pytest.raises(DatabaseConnectionError) as exc_info:
        db.connect()
    assert "not specified" in str(exc_info.value)


def test_database_invalid_credentials_raises_auth_error():
    invalid_url = "postgresql://postgres.nvovpmyzxxermklmpvuk:wrong_password@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    db = Database(database_url=invalid_url)
    with pytest.raises(DatabaseAuthenticationError):
        db.connect()
