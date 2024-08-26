from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.api.url_generator import get_api_url
import time

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/generate_url/")
async def generate_url(request: QueryRequest):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            api_url = get_api_url(request.query)
            return {"response": api_url}
        except Exception as e:
            if attempt < max_retries - 1:  # If not the last attempt, wait and retry
                continue
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed after {max_retries} attempts: {str(e)}"
            )