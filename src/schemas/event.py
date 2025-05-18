from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    status: str
    created_at: datetime
    is_bitrix: bool
    user_id: int

    class Config:
        from_attributes = True 