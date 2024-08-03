import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.url_generator import get_api_url

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # Fixes import errors


router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/generate_url/")
async def generate_url(request: QueryRequest):
    try:
        api_url = get_api_url(request.query)
        return {"api_url": api_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
