from datetime import date
from enum import Enum
from sqlalchemy import String, Date, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WorkStatus(str, Enum):
    IN_OFFICE = "в офисе"
    REMOTE = "удаленно"
    ON_LEAVE = "на выходных"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    work_status: Mapped[WorkStatus] = mapped_column(SQLEnum(WorkStatus), default=WorkStatus.IN_OFFICE)
    
    # Контактные данные
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20))
    
    # Фото профиля (путь к файлу)
    profile_photo: Mapped[str] = mapped_column(String(255))
    
    # Раздел "О себе"
    about: Mapped[str] = mapped_column(Text)
    hobbies: Mapped[str] = mapped_column(Text)
    skills: Mapped[str] = mapped_column(Text)
    preferences: Mapped[str] = mapped_column(Text) 