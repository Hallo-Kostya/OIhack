from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import String, Date, Enum as SQLEnum, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import datetime

class Projects_Workers(Base):
    __tablename__ = "workers_projects"
    worker_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id",ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String, default="member")  
    joined_at: Mapped[DateTime] =  mapped_column(DateTime, default=datetime.now())



class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="owned_projects")
    workers: Mapped[List["User"]] = relationship(back_populates="projects", secondary="workers_projects")  
   
