from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.schemas.employee import EmployeeResponse
from src.database.session import async_session_factory
from src.services.bitrix import Bitrix24API, get_bitrix_api
from src.models.user import User

router = APIRouter()

@router.post("/auth/find-employee", response_model=EmployeeResponse)
async def find_employee(
    email: str,
    bitrix: Bitrix24API = Depends(get_bitrix_api)
):
    """
    Ищет сотрудника в Bitrix24 по email.
    Если сотрудник найден, возвращает запись из БД.
    """
    async with async_session_factory() as session:
        try:
            employees = session.get(User)
            
            if not employees:
                raise HTTPException(
                    status_code=404,
                    detail="Сотрудник не найден в Bitrix24"
                )
            
            matching_employee = None
            for employee in employees:
                if employee.get('email') == email:
                    matching_employee = employee
                    break
            
            if not matching_employee:
                raise HTTPException(
                    status_code=404,
                    detail="Сотрудник не найден в Bitrix24"
                )
            
            employee = session.get(User, matching_employee['id'])
            
            if not employee:
                raise HTTPException(
                    status_code=404,
                    detail="Сотрудник не найден в БД"
                )
            
            return employee

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при поиске сотрудника: {str(e)}"
            )
