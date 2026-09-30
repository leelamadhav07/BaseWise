from app.dependencies.database import get_database
from app.services.schema_service import SchemaService
from app.services.llm_service import LLMService
from app.services.sql_safety_service import SQLSafetyService
from app.services.sql_execution_service import SQLExecutionService, SQLExecutionError


class QueryService:
    def __init__(self):
        self.llm_service = LLMService()
        self.sql_safety_service = SQLSafetyService()
        self.sql_execution_service = SQLExecutionService()

    def process_question(self, question: str) -> dict:
        database = get_database()
        schema_service = SchemaService(database)
        schema = schema_service.get_schema()

        sql = self.llm_service.generate_sql(
            question=question,
            schema=schema
        )

        is_safe, message = self.sql_safety_service.validate(sql)
        if not is_safe:
            # Query rejected by security validation layer: DO NOT execute against database
            return {
                "question": question,
                "sql": sql,
                "safe": False,
                "message": message,
                "result": None,
            }

        # SQL passed safety checks: execute query
        try:
            result = self.sql_execution_service.execute(database, sql)
            return {
                "question": question,
                "sql": sql,
                "safe": True,
                "message": message,
                "result": result,
            }
        except SQLExecutionError as e:
            return {
                "question": question,
                "sql": sql,
                "safe": True,
                "message": str(e),
                "result": None,
            }