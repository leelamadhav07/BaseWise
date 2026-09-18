from fastapi import APIRouter
from app.services.schema_service import SchemaService
from app.dependencies.database import get_database


router = APIRouter(
    prefix = "/schema",
    tags=["schema"]
    )

@router.get("/")
def get_schema():
    database = get_database()
    schema_service = SchemaService(database)
    return schema_service.get_schema()
 