from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import String, Date, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.event import Event

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    project: Mapped[set] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    profile_photo: Mapped[str] = mapped_column(String(255),nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    events: Mapped[List["Event"]] = relationship("Event", back_populates="user", cascade="all, delete-orphan")