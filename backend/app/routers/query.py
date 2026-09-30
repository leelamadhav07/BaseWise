from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)

query_service = QueryService()


@router.post("/", response_model=QueryResponse)
def process_query(request: QueryRequest):

    return query_service.process_question(request.question)