from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import List
from sqlalchemy import select
from src.database.session import async_session_factory
from src.models.event import Event
from src.models.user import User
from src.schemas.event import EventCreate

calendar_router = APIRouter()

@calendar_router.get("/events")
async def get_events():
    """
    Получает все события из БД.
    """
    try:
        async with async_session_factory() as session:
            stmt = select(Event)
            result = await session.execute(stmt)
            events = result.scalars().all()
            
            # Преобразуем события в формат для календаря
            calendar_events = []
            for event in events:
                calendar_events.append({
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_date.isoformat(),
                    "end": event.end_date.isoformat(),
                    "description": event.description,
                    "location": event.location,
                    "is_bitrix": event.is_bitrix,
                    "user_id": event.user_id
                })
            
            print(f"Найдено событий: {len(calendar_events)}")
            return calendar_events
            
    except Exception as e:
        print(f"Ошибка при получении событий: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import Query

from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: str  # Ожидается в формате "YYYY-MM-DDTHH:MM:SSZ"
    end_date: str
    location: Optional[str] = None

    @validator('start_date', 'end_date')
    def validate_dates(cls, v):
        try:
            # Пробуем разные форматы дат
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(v, fmt)
                except ValueError:
                    continue
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DDTHH:MM:SSZ")
        except Exception as e:
            raise ValueError(f"Ошибка преобразования даты: {str(e)}")

from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: str  # Ожидается в формате "YYYY-MM-DDTHH:MM:SSZ"
    end_date: str
    location: Optional[str] = None

    @validator('start_date', 'end_date')
    def validate_dates(cls, v):
        try:
            # Пробуем разные форматы дат
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(v, fmt)
                except ValueError:
                    continue
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DDTHH:MM:SSZ")
        except Exception as e:
            raise ValueError(f"Ошибка преобразования даты: {str(e)}")

@calendar_router.post("/addevent")
async def create_event(
    event_data: EventCreate,
    user_id: int = Query(..., gt=0)
):
    try:
        async with async_session_factory() as session:
            # Проверка пользователя
            user = await session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            # Даты уже преобразованы валидатором
            new_event = Event(
                title=event_data.title,
                description=event_data.description,
                start_date=event_data.start_date,  # Теперь это datetime
                end_date=event_data.end_date,      # Теперь это datetime
                location=event_data.location,
                user_id=user_id
            )
            
            session.add(new_event)
            await session.commit()
            await session.refresh(new_event)
            
            return {
                "id": new_event.id,
                "title": new_event.title,
                "start": new_event.start_date.isoformat(),
                "end": new_event.end_date.isoformat(),
                "description": new_event.description,
                "location": new_event.location,
                "is_bitrix": False,
                "user_id": new_event.user_id
            }
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@calendar_router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    """
    Удаляет событие из БД.
    """
    try:
        async with async_session_factory() as session:
            stmt = select(Event).where(Event.id == event_id)
            result = await session.execute(stmt)
            event = result.scalar_one_or_none()
            
            if not event:
                raise HTTPException(
                    status_code=404,
                    detail="Событие не найдено"
                )
            
            await session.delete(event)
            await session.commit()
            
            return {"message": "Событие успешно удалено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))