# Milestone 3 — Schema Introspection

# The purpose of this milestone is:
# Basewise should automatically discover what's inside the connected database.

class SchemaService:
    """Handles database schema introspection."""

    def __init__(self, database):
        self.database = database

    def get_tables(self, schema_name: str = "public"):
        """Return all base tables in the specified schema (defaults to 'public')."""

        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """

        with self.database.connection.cursor() as cursor:
            cursor.execute(query, (schema_name,))
            rows = cursor.fetchall()

        return [row[0] for row in rows]
    
    def get_columns(self):
        """Return columns and data types for all public tables."""

        query = """
    SELECT
        table_name,
        column_name,
        data_type,
        is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """

        with self.database.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        schema = {}

        for table_name, column_name, data_type, is_nullable in rows:
            if table_name not in schema:
                schema[table_name] = []

            schema[table_name].append({
                "name": column_name,
                "type": data_type,
                "nullable": is_nullable == "YES"
            })

        return schema