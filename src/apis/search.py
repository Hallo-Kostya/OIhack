from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from typing import List, Dict, Any

from models.user import User
from models.event import Event
from services.gigachat_service import GigaChatService
from database import get_db

router = APIRouter()
gigachat_service = GigaChatService()

@router.post("/search")
async def intelligent_search(query: str) -> Dict[str, Any]:
    # Анализируем запрос с помощью GigaChat
    analysis = await gigachat_service.analyze_query(query)
    
    results = []
    
    # Поиск по пользователям
    if analysis["search_type"] in ["users", "all"]:
        user_query = select(User).where(
            or_(
                User.full_name.ilike(f"%{term}%") for term in analysis["search_criteria"]
            )
        )
        users = await db.execute(user_query)
        results.extend([{
            "type": "user",
            "data": user.__dict__
        } for user in users.scalars().all()])
    
    # Поиск по мероприятиям
    if analysis["search_type"] in ["events", "all"]:
        event_query = select(Event)
        
        # Фильтр по времени
        if analysis["time_period"] == "past":
            event_query = event_query.where(Event.end_date < datetime.now())
        elif analysis["time_period"] == "future":
            event_query = event_query.where(Event.start_date > datetime.now())
            
        # Фильтр по местоположению
        if analysis["location"]:
            event_query = event_query.where(Event.location.ilike(f"%{analysis['location']}%"))
            
        # Поиск по ключевым словам
        event_query = event_query.where(
            or_(
                Event.title.ilike(f"%{term}%") for term in analysis["search_criteria"]
            )
        )
        
        events = await db.execute(event_query)
        results.extend([{
            "type": "event",
            "data": event.__dict__
        } for event in events.scalars().all()])
    
    # Генерируем естественный ответ
    response = await gigachat_service.generate_response(results, query)
    
    return {
        "query": query,
        "analysis": analysis,
        "results": results,
        "response": response
    } 