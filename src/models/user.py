from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import String, Date, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.event import Event


class WorkStatus(str, Enum):
    IN_OFFICE = "в офисе"
    REMOTE = "удаленно"
    ON_LEAVE = "на выходных"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    work_status: Mapped[WorkStatus] = mapped_column(SQLEnum(WorkStatus), default=WorkStatus.IN_OFFICE)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    profile_photo: Mapped[str] = mapped_column(String(255),nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    hobbies: Mapped[str] = mapped_column(Text,nullable=True)
    skills: Mapped[str] = mapped_column(Text,nullable=True)
    preferences: Mapped[str] = mapped_column(Text,nullable=True) 
    events: Mapped[List["Event"]] = relationship(back_populates="organizer", cascade="all, delete-orphan")