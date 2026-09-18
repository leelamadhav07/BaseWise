import sys
from pathlib import Path

# Add backend directory to sys.path dynamically for robust cross-platform imports
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from basewise.database import Database
from app.services.schema_service import SchemaService


db = Database()

try:
    db.connect()

    schema = SchemaService(db)

    # tables = schema.get_tables()
    # columns = schema.get_columns()

    # print("Tables found:")
    
    # for table in tables:
    #     print("-", table)
    
    # print("\nColumns:")

    # for table, table_columns in columns.items():
    #     print(f"\n{table}:")

    #     for column in table_columns:
    #         print(
    #             f"  - {column['name']} "
    #             f"({column['type']}, "
    #             f"nullable={column['nullable']})"
    #         )
    # print("\nRelationships:")
    # relationships = schema.get_relationships()
    # for rel in relationships:
    #     print(
    #         f"  - {rel['table']}.{rel['column']} "
    #         f"-> {rel['references_table']}.{rel['references_column']}"
    #     )
    schema_data = schema.get_schema()

    print("\nComplete Schema:")

    for table_name, table_info in schema_data["tables"].items():

        print(f"\nTable: {table_name}")

        print("Columns:")

        for column in table_info["columns"]:
            print(
                f"  - {column['name']} "
                f"({column['type']}, "
                f"nullable={column['nullable']})"
            )

        print("Foreign Keys:")

        for foreign_key in table_info["foreign_keys"]:
            print(
                f"  - {foreign_key['column']} → "
                f"{foreign_key['references_table']}."
                f"{foreign_key['references_column']}"
            )

finally:
    db.close()