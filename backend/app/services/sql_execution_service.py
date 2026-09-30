import psycopg2


class SQLExecutionError(Exception):
    """Raised when query execution against the database fails."""
    pass


class SQLExecutionService:
    """Handles execution of validated read-only SQL queries."""

    def execute(self, database, sql: str) -> dict:
        """
        Executes a validated read-only SQL query against the connected database.
        Returns a dictionary with columns, rows, and row_count.
        """
        if not database.is_connected():
            database.connect()

        connection = database.connection
        if not connection:
            raise SQLExecutionError("Database connection is not available.")

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql)

            if cursor.description is not None:
                columns = [desc[0] for desc in cursor.description]
                raw_rows = cursor.fetchall()
                # Ensure rows are JSON-serializable list of lists
                rows = [list(row) for row in raw_rows]
            else:
                columns = []
                rows = []

            # Cleanly commit read transaction to release locks and avoid hanging transactions
            connection.commit()

            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
            }
        except psycopg2.Error as e:
            if connection:
                try:
                    connection.rollback()
                except Exception:
                    pass
            err_msg = getattr(e, "pgerror", None) or str(e)
            raise SQLExecutionError(f"Database error executing query: {err_msg.strip()}") from e
        except Exception as e:
            if connection:
                try:
                    connection.rollback()
                except Exception:
                    pass
            raise SQLExecutionError(f"Failed to execute query: {str(e).strip()}") from e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass