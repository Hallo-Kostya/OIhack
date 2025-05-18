from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    start_time: str
    end_time: str
    description: Optional[str] = None
    location: Optional[str] = None

class EventCreate(EventBase):
    user_id: int

class EventResponse(EventBase):
    id: str
    is_bitrix: bool

    class Config:
        from_attributes = True 