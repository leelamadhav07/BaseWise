from fastapi import APIRouter, HTTPException

from app.schemas.database import (
    DatabaseConnectionRequest,
    DatabaseConnectionResponse
)

from app.dependencies.database import connect_user_database
from app.core.config import settings


router = APIRouter(
    prefix="/database",
    tags=["Database"]
)


@router.post(
    "/connect",
    response_model=DatabaseConnectionResponse
)
def connect_database(request: DatabaseConnectionRequest):

    try:
        db_url = request.database_url
        if not db_url or db_url == "string":
            db_url = settings.DATABASE_URL

        if not db_url:
            raise ValueError("No database URL provided and default DATABASE_URL is not set.")

        connect_user_database(db_url)

        return DatabaseConnectionResponse(
            success=True,
            message="Database connected successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Database connection failed: {str(e)}"
        )