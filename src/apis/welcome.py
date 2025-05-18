from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.database.session import get_db
from src.services.welcome import WelcomeService
from src.services.bitrix import get_bitrix_api
from src.models.welcome import Gender

router = APIRouter()

class WelcomeFormRequest(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime
    gender: Gender

class WelcomeFormResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime
    gender: Gender
    employee_id: Optional[int] = None

    class Config:
        from_attributes = True

@router.post("/welcome", response_model=WelcomeFormResponse)
async def create_welcome_form(
    form_data: WelcomeFormRequest,
    db: Session = Depends(get_db),
    bitrix = Depends(get_bitrix_api)
):
    """Создает приветственную форму и связывает с сотрудником из Bitrix24"""
    service = WelcomeService(db, bitrix)
    
    try:
        form = await service.process_welcome_form(
            first_name=form_data.first_name,
            last_name=form_data.last_name,
            birth_date=form_data.birth_date,
            gender=form_data.gender
        )
        return form
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке формы: {str(e)}"
        )

@router.get("/welcome/{form_id}", response_model=WelcomeFormResponse)
def get_welcome_form(
    form_id: int,
    db: Session = Depends(get_db),
    bitrix = Depends(get_bitrix_api)
):
    """Получает форму по ID"""
    service = WelcomeService(db, bitrix)
    form = service.get_form_by_id(form_id)
    
    if not form:
        raise HTTPException(
            status_code=404,
            detail="Форма не найдена"
        )
    
    return form

@router.get("/welcome/employee/{employee_id}", response_model=list[WelcomeFormResponse])
def get_employee_forms(
    employee_id: int,
    db: Session = Depends(get_db),
    bitrix = Depends(get_bitrix_api)
):
    """Получает все формы сотрудника"""
    service = WelcomeService(db, bitrix)
    return service.get_forms_by_employee(employee_id) 