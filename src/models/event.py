from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from .base import Base

class Events_users(Base):
    __tablename__ = "events_users"
    member_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    joined_at: Mapped[DateTime] =  mapped_column(DateTime, default=datetime.now())


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(50), default="active")
    members: Mapped[List["User"]] = relationship(back_populates="events", secondary="events_users")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow) 
    organizer: Mapped["User"] = relationship(back_populates="owned_events")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "organizer_id": self.organizer_id,
            "members": [member.name for member in self.members]
        }
    def __str__(self):
        return f"Задача: {self.title}, начало:{self.start_date} конец: {self.end_date}"