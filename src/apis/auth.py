from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select
from src.database.session import async_session_factory
from src.services.bitrix import Bitrix24API, get_bitrix_api
from src.models.user import User
from pydantic import BaseModel, EmailStr

auth_router = APIRouter()

@auth_router.get("/auth/find-employee")
async def find_employee(
    email: str,
):
    """
    Ищет сотрудника в БД по email.
    """
    async with async_session_factory() as session:
        try:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            employee = result.scalar_one_or_none()
            
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail="Сотрудник не найден в БД"
                )
            
            return User(
                id=employee.id,
                first_name=employee.first_name,
                last_name=employee.last_name,
                birth_date=employee.birth_date,
                department=employee.department,
                project=employee.project,
                email=employee.email,
                phone=employee.phone,
                profile_photo=employee.profile_photo,
                about=employee.about
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при поиске сотрудника: {str(e)}"
            )
