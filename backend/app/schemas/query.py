from typing import Any
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    schema: Any
    sql: str
#Schema aware text to SQL