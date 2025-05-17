from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import String, Date, Enum as SQLEnum, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class WorkStatus(str, Enum):
    IN_OFFICE = "в офисе"
    REMOTE = "удаленно"
    ON_LEAVE = "на выходных"

class WorkRole(str, Enum):
    HR = "HR"
    MANAGER = "MANAGER"
    WORKER = "WORKER"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    role: Mapped[WorkStatus] = mapped_column(SQLEnum(WorkRole), default=WorkRole.WORKER)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    department: Mapped["Department"] = relationship(back_populates="workers")
    work_status: Mapped[WorkStatus] = mapped_column(SQLEnum(WorkStatus), default=WorkStatus.IN_OFFICE)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    profile_photo: Mapped[str] = mapped_column(String(255),nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    hobbies: Mapped[str] = mapped_column(Text,nullable=True)
    skills: Mapped[str] = mapped_column(Text,nullable=True)
    preferences: Mapped[str] = mapped_column(Text,nullable=True) 
    owned_events: Mapped[List["Event"]] = relationship(back_populates="organizer", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="workers", secondary="workers_projects")
    owned_projects: Mapped[List["Project"]] = relationship("Project", back_populates="owner")
    events: Mapped[List["Event"]] = relationship(back_populates="members", secondary="events_users")
    tasks: Mapped[List["Task"]] = relationship(secondary="tasks_users", back_populates="task_workers")
    owned_tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

