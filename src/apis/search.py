from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from typing import List, Dict, Any
import requests
from config import settings
from models.user import User
from models.event import Event
from services.gigachat_service import GigaChatService
from .service import analyze_query


router = APIRouter()


@router.get("/search")
async def search(query: str):
    # Анализируем запрос с помощью GigaChat
    return analyze_query(query)