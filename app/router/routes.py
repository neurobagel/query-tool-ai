from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.api.url_generator import get_api_url


router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/generate_url/")
async def generate_url(request: QueryRequest):
    try:
        api_url = get_api_url(request.query)
        return {"response": api_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
