import re
from fastapi import APIRouter, HTTPException

from app.schemas.database import (
    DatabaseConnectionRequest,
    DatabaseConnectionResponse
)
from app.services.database_service import DatabaseService


router = APIRouter(
    prefix="/database",
    tags=["Database"]
)

database_service = DatabaseService()


def sanitize_error_message(msg: str) -> str:
    """Remove sensitive password patterns from error messages."""
    return re.sub(r':([^/@:\s]+)@', ':****@', msg)


@router.post(
    "/connect",
    response_model=DatabaseConnectionResponse
)
def connect_database(request: DatabaseConnectionRequest):

    try:
        db = database_service.connect(request.database_url)
        if db:
            db.close()

        return DatabaseConnectionResponse(
            success=True,
            message="Database connected successfully"
        )

    except Exception as e:
        safe_detail = sanitize_error_message(str(e))
        raise HTTPException(
            status_code=400,
            detail=f"Database connection failed: {safe_detail}"
        )