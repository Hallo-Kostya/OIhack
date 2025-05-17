from fastapi import APIRouter
from .service import analyze_query


router = APIRouter()


@router.get("/search")
async def search(query: str):
    # Анализируем запрос с помощью GigaChat
    return analyze_query(query)