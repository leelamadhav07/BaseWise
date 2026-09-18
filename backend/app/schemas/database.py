from typing import Optional
from pydantic import BaseModel, Field


class DatabaseConnectionRequest(BaseModel):
    database_url: Optional[str] = Field(
        default=None,
        description="PostgreSQL connection URL. If omitted, empty, or 'string', uses default project settings."
    )


class DatabaseConnectionResponse(BaseModel):
    success: bool
    message: str