from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.user import User

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_bitrix: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="events")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "location": self.location,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "is_bitrix": self.is_bitrix,
            "user_id": self.user_id,
            "user": {
                "id": self.user.id,
                "name": f"{self.user.first_name} {self.user.last_name}",
                "email": self.user.email
            } if self.user else None
        }