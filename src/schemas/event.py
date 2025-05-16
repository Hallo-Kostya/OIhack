from pydantic import BaseModel

class EventCreateBase(BaseModel):
    title: str
    organizer_id: int
