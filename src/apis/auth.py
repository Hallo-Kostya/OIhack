from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.schemas.employee import EmployeeResponse, EmployeeSearchRequest, Gender
from src.database.session import async_session_factory
from src.services.bitrix import Bitrix24API, get_bitrix_api
from src.models.user import User

router = APIRouter()

@router.post("/auth/find-employee", response_model=EmployeeResponse)
async def find_employee(
    first_name: str,
    last_name: str,
    birth_date: datetime,
    gender: Gender,
    bitrix: Bitrix24API = Depends(get_bitrix_api)
):
    """
    Ищет сотрудника в Bitrix24 по имени, фамилии, дате рождения и полу.
    Если сотрудник найден, создает или обновляет запись в БД.
    """
    async with async_session_factory() as session:
        try:
            bitrix_employees = await bitrix.find_employees(
                first_name=first_name,
                last_name=last_name
            )
            
            if not bitrix_employees:
                raise HTTPException(
                    status_code=404,
                    detail="Сотрудник не найден в Bitrix24"
                )

            bitrix_gender = {
                Gender.MALE: "M",
                Gender.FEMALE: "F",
                Gender.OTHER: "N"
            }.get(gender)
            
            matching_employee = None
            for employee in bitrix_employees:
                if bitrix_gender and employee.get('gender') and employee['gender'] != bitrix_gender:
                    continue

                if employee.get('birth_date'):
                    try:
                        bitrix_birth_date = datetime.strptime(employee['birth_date'], '%Y-%m-%d')
                        if bitrix_birth_date.date() != birth_date.date():
                            continue
                    except (ValueError, TypeError):
                        pass
                
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
                    detail="Сотрудник не найден в Bitrix24"
                )
            
            return employee

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при поиске сотрудника: {str(e)}"
            )
