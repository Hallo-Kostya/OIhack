from sqlalchemy import String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.database.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    crm_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str | None] = mapped_column(String(255))
    department: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    last_sync: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user_events: Mapped[list["UserEvent"]] = relationship(back_populates="employee")
    bitrix_events: Mapped[list["BitrixEvent"]] = relationship(back_populates="employee")

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, name='{self.name}', crm_id={self.crm_id})>"

class UserEvent(Base):
    __tablename__ = "user_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(nullable=False)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    # Отношения
    employee: Mapped["Employee"] = relationship(back_populates="user_events")

    def __repr__(self) -> str:
        return f"<UserEvent(id={self.id}, title='{self.title}', start_time={self.start_time})>"

class BitrixEvent(Base):
    __tablename__ = "bitrix_events"
    __table_args__ = (
        UniqueConstraint('bitrix_id', name='uq_bitrix_event_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bitrix_id: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"))
    last_sync: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    # Отношения
    employee: Mapped["Employee"] = relationship(back_populates="bitrix_events")

    def __repr__(self) -> str:
        return f"<BitrixEvent(id={self.id}, title='{self.title}', bitrix_id='{self.bitrix_id}')>"

    @classmethod
    def from_bitrix_data(cls, bitrix_data: dict, employee_id: int) -> "BitrixEvent":
        """Создает или обновляет событие из данных Bitrix24"""
        return cls(
            bitrix_id=str(bitrix_data.get('id')),
            title=bitrix_data.get('name', ''),
            start_time=datetime.fromisoformat(bitrix_data.get('from')),
            end_time=datetime.fromisoformat(bitrix_data.get('to')),
            description=bitrix_data.get('description', ''),
            location=bitrix_data.get('location', ''),
            employee_id=employee_id,
            last_sync=datetime.utcnow()
        ) 