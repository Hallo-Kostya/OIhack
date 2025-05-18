from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.apis.bitrix24 import Bitrix24API
from src.config import settings
from src.database.session import async_session_factory
from src.models.calendar import UserEvent, Employee
from src.schemas.calendar import EventCreate, EventResponse
from src.services.calendar_sync import CalendarSyncService

router = APIRouter()
bitrix = Bitrix24API(settings.BITRIX24_WEBHOOK_URL)
calendar_sync = CalendarSyncService(bitrix)

@router.get("/api/events", response_model=List[EventResponse])
async def get_events(date: str = None):
    try:
        if date:
            start_date = datetime.strptime(date, '%Y-%m-%d')
        else:
            start_date = datetime.now()
        
        end_date = start_date + timedelta(days=30)
        
        async with async_session_factory() as session:
            # Получаем пользовательские события
            user_events = await session.execute(
                select(UserEvent).filter(
                    UserEvent.start_time >= start_date,
                    UserEvent.end_time <= end_date
                )
            )
            user_events = user_events.scalars().all()
            
            # Формируем список событий
            all_events = []
            
            # Добавляем пользовательские события
            for event in user_events:
                event_data = {
                    "id": f"user_{event.id}",
                    "title": event.title,
                    "start_time": event.start_time.isoformat(),
                    "end_time": event.end_time.isoformat(),
                    "description": event.description,
                    "location": event.location,
                    "is_bitrix": False
                }
                
                # Если событие связано с сотрудником, добавляем информацию о нем
                if event.employee_id:
                    employee = await session.get(Employee, event.employee_id)
                    if employee:
                        event_data["employee"] = {
                            "id": employee.id,
                            "name": employee.name,
                            "position": employee.position,
                            "department": employee.department
                        }
                
                all_events.append(event_data)
            
            return all_events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/events", response_model=EventResponse)
async def create_event(event_data: EventCreate):
    try:
        async with async_session_factory() as session:
            new_event = UserEvent(
                title=event_data.title,
                start_time=datetime.fromisoformat(event_data.start_time),
                end_time=datetime.fromisoformat(event_data.end_time),
                description=event_data.description,
                location=event_data.location,
                user_id=event_data.user_id,
                employee_id=event_data.employee_id
            )
            
            session.add(new_event)
            await session.commit()
            await session.refresh(new_event)
            
            response_data = {
                "id": f"user_{new_event.id}",
                "title": new_event.title,
                "start_time": new_event.start_time.isoformat(),
                "end_time": new_event.end_time.isoformat(),
                "description": new_event.description,
                "location": new_event.location,
                "is_bitrix": False
            }
            
            # Если событие связано с сотрудником, добавляем информацию о нем
            if new_event.employee_id:
                employee = await session.get(Employee, new_event.employee_id)
                if employee:
                    response_data["employee"] = {
                        "id": employee.id,
                        "name": employee.name,
                        "position": employee.position,
                        "department": employee.department
                    }
            
            return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/events/{event_id}")
async def delete_event(event_id: str):
    try:
        if not event_id.startswith('user_'):
            raise HTTPException(
                status_code=400,
                detail="Можно удалять только пользовательские события"
            )
        
        event_db_id = int(event_id.split('_')[1])
        
        async with async_session_factory() as session:
            event = await session.get(UserEvent, event_db_id)
            if not event:
                raise HTTPException(status_code=404, detail="Событие не найдено")
            
            await session.delete(event)
            await session.commit()
            
            return {"message": "Событие успешно удалено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/employees")
async def get_employees():
    """
    Получает список сотрудников
    """
    try:
        async with async_session_factory() as session:
            employees = await calendar_sync.get_employees(session)
            return [
                {
                    "id": emp.id,
                    "name": emp.name,
                    "position": emp.position,
                    "department": emp.department,
                    "email": emp.email,
                    "phone": emp.phone
                }
                for emp in employees
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/employees/sync")
async def sync_employees():
    """
    Эндпоинт для ручной синхронизации сотрудников из CRM
    """
    try:
        async with async_session_factory() as session:
            await calendar_sync.sync_employees(session)
            return {"message": "Синхронизация сотрудников успешно завершена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 