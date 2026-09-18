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
    def get_relationships(self):
        """Return primary key and foreign key relationships."""

        query = """
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS referenced_table,
            ccu.column_name AS referenced_column
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'public'
        ORDER BY tc.table_name, kcu.column_name;
        """

        with self.database.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        relationships = []

        for table, column, referenced_table, referenced_column in rows:
            relationships.append({
                "table": table,
                "column": column,
                "references_table": referenced_table,
                "references_column": referenced_column
            })

        return relationships

    def get_schema(self):
        """Return the complete database schema."""

        tables = self.get_tables()
        columns = self.get_columns()
        relationships = self.get_relationships()
        schema = {
            "tables": {}
        }

        # Add tables and their columns
        for table in tables:
            schema["tables"][table] = {
                "columns": columns.get(table, []),
                "primary_keys": [],
                "foreign_keys": []
            }

        # Add foreign-key relationships
        for relationship in relationships:
            table = relationship["table"]

            if table in schema["tables"]:
                schema["tables"][table]["foreign_keys"].append({
                    "column": relationship["column"],
                    "references_table": relationship["references_table"],
                    "references_column": relationship["references_column"]
                })

        return schema