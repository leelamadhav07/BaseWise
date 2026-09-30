import pytest
from app.services.sql_safety_service import SQLSafetyService


@pytest.fixture
def safety_service():
    return SQLSafetyService()


def test_safety_allows_valid_select(safety_service):
    is_safe, msg = safety_service.validate("SELECT * FROM customers;")
    assert is_safe is True
    assert "safe" in msg.lower() or "passed" in msg.lower()


def test_safety_allows_select_with_where_and_order(safety_service):
    is_safe, msg = safety_service.validate("SELECT id, name FROM customers WHERE city = 'Delhi' ORDER BY id ASC")
    assert is_safe is True


def test_safety_allows_union_select(safety_service):
    is_safe, msg = safety_service.validate("SELECT id FROM customers UNION SELECT id FROM orders")
    assert is_safe is True


def test_safety_rejects_empty(safety_service):
    is_safe, msg = safety_service.validate("")
    assert is_safe is False
    assert "empty" in msg.lower()

    is_safe, msg = safety_service.validate("   \n\t  ")
    assert is_safe is False
    assert "empty" in msg.lower()


def test_safety_rejects_drop(safety_service):
    is_safe, msg = safety_service.validate("DROP TABLE customers;")
    assert is_safe is False
    assert "select" in msg.lower() or "drop" in msg.lower()


def test_safety_rejects_delete(safety_service):
    is_safe, msg = safety_service.validate("DELETE FROM customers WHERE id = 1;")
    assert is_safe is False


def test_safety_rejects_update(safety_service):
    is_safe, msg = safety_service.validate("UPDATE customers SET name = 'Hacked';")
    assert is_safe is False


def test_safety_rejects_insert(safety_service):
    is_safe, msg = safety_service.validate("INSERT INTO customers (name) VALUES ('Hacked');")
    assert is_safe is False


def test_safety_rejects_alter(safety_service):
    is_safe, msg = safety_service.validate("ALTER TABLE customers ADD COLUMN hack TEXT;")
    assert is_safe is False


def test_safety_rejects_truncate(safety_service):
    is_safe, msg = safety_service.validate("TRUNCATE TABLE customers;")
    assert is_safe is False


def test_safety_rejects_create(safety_service):
    is_safe, msg = safety_service.validate("CREATE TABLE hack (id INT);")
    assert is_safe is False


def test_safety_rejects_grant(safety_service):
    is_safe, msg = safety_service.validate("GRANT ALL PRIVILEGES ON customers TO public;")
    assert is_safe is False


def test_safety_rejects_revoke(safety_service):
    is_safe, msg = safety_service.validate("REVOKE ALL ON customers FROM public;")
    assert is_safe is False


def test_safety_rejects_multiple_statements(safety_service):
    is_safe, msg = safety_service.validate("SELECT * FROM customers; DROP TABLE customers;")
    assert is_safe is False
    assert "multiple" in msg.lower()


def test_safety_rejects_sql_comments(safety_service):
    is_safe, msg = safety_service.validate("SELECT * FROM customers -- inline comment")
    assert is_safe is False
    assert "comment" in msg.lower()

    is_safe, msg = safety_service.validate("SELECT /* block comment */ * FROM customers")
    assert is_safe is False
    assert "comment" in msg.lower()


def test_safety_rejects_nested_cte_dml(safety_service):
    is_safe, msg = safety_service.validate("WITH deleted AS (DELETE FROM customers RETURNING *) SELECT * FROM deleted")
    assert is_safe is False


def test_safety_rejects_select_into(safety_service):
    is_safe, msg = safety_service.validate("SELECT * INTO new_table FROM customers")
    assert is_safe is False
