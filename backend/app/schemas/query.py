from typing import Any, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str


class QueryExecutionResult(BaseModel):
    columns: list[str] = Field(default_factory=list)
    rows: list[Any] = Field(default_factory=list)
    row_count: int = 0


class QueryResponse(BaseModel):
    question: str
    sql: str
    safe: bool
    message: str
    result: Optional[QueryExecutionResult] = None
    schema_: Optional[Any] = Field(default=None, alias="schema")

    class Config:
        populate_by_name = True