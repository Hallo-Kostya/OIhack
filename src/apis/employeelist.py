from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy import or_, select
from src.database.session import async_session_factory
from src.models.user import User

list_router = APIRouter()

@list_router.get("/employees")
async def get_employees(
    name: Optional[str] = None,
    department: Optional[str] = None,
    project: Optional[str] = None,
):
    """
    Получает список сотрудников из базы данных.
    Поддерживает фильтрацию по отделу, имени и проекту.
    """
    async with async_session_factory() as session:
        try:
            # Создаем базовый запрос
            stmt = select(User)
            
            # Применяем фильтры, если они указаны
            if department:
                stmt = stmt.where(User.department == department)
            if project:
                stmt = stmt.where(User.project == project)
            if name:
                # Ищем по имени или фамилии
                stmt = stmt.where(
                    or_(
                        User.first_name.ilike(f"%{name}%"),
                        User.last_name.ilike(f"%{name}%"),
                        User.first_name.concat(" ").concat(User.last_name).ilike(f"%{name}%")
                    )
                )
            
            # Выполняем запрос
            result = await session.execute(stmt)
            users = result.scalars().all()
            
            return users
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении списка сотрудников: {str(e)}"
            )

@list_router.get("/employees/{employee_id}")
async def get_employee(
    employee_id: int,
):
    """
    Получает информацию о конкретном сотруднике по его ID.
    """
    async with async_session_factory() as session:
        try:
            stmt = select(User).where(User.id == employee_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="Сотрудник не найден"
                )
                
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении информации о сотруднике: {str(e)}"
            )
