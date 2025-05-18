from fastapi import APIRouter
from src.schemas.user import UserBase
from src.schemas.event import EventCreateBase
from src.models import User, Event
from src.database.session import async_session_factory

router = APIRouter()

@router.post("/user/register")
async def register_user(
    data: UserBase
):
    async with async_session_factory() as session:
        user = User(**data.model_dump(mode="json"))
        session.add(user)
        await session.commit()
    return data

@router.post("/events")
async def add_event(
    data: EventCreateBase
):
    async with async_session_factory() as session:
        event = Event(**data.model_dump(mode="json"))
        session.add(event)
        await session.commit()
    return data