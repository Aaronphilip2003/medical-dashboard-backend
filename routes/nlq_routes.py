from fastapi import APIRouter
from database.connection import client
from utils.query_processor import process_natural_query

router = APIRouter()

@router.post("/query")
async def natural_language_query(body: dict):
    result = process_natural_query(body["question"])
    if not result["success"]:
        return {"error": result["error"]}
    return result 