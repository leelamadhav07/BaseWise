from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)

query_service = QueryService()


@router.post("/", response_model=QueryResponse, response_model_exclude_none=True)
def process_query(request: QueryRequest):
    try:
        return query_service.process_question(request.question)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process query: {str(e)}"
        )