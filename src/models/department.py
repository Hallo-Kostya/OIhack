from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import String, Date, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    workers: Mapped[List["User"]] = relationship(back_populates="department", cascade="all, delete-orphan")