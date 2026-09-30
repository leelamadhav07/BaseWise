from app.dependencies.database import get_database
from app.services.schema_service import SchemaService
from app.services.llm_service import LLMService

class QueryService:
    def __init__(self):
        self.llm_service = LLMService()
    def process_question(self, question: str):
        database = get_database()
        schema_service = SchemaService(database)
        schema = schema_service.get_schema()
        sql = self.llm_service.generate_sql(
            question=question,
            schema=schema
        )
        return {
            "question": question,
            "schema": schema,
            "sql": sql
        }
# preparing schema context, llm implementation