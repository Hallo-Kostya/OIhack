from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from src.models.welcome import WelcomeForm, Gender
from src.models.calendar import Employee
from src.services.bitrix import Bitrix24API

class WelcomeService:
    def __init__(self, db: Session, bitrix: Bitrix24API):
        self.db = db
        self.bitrix = bitrix

    async def find_employee_in_bitrix(
        self,
        first_name: str,
        last_name: str,
        birth_date: datetime,
        gender: Gender
    ) -> Optional[Dict]:
        """
        Ищет сотрудника в Bitrix24 по имени, фамилии, дате рождения и полу.
        Возвращает данные сотрудника, если найден точный совпадение.
        """
        try:
            # Ищем сотрудников по имени и фамилии
            bitrix_employees = await self.bitrix.find_employees(
                first_name=first_name,
                last_name=last_name
            )
            
            if not bitrix_employees:
                return None

            # Преобразуем пол в формат Bitrix24
            bitrix_gender = {
                Gender.MALE: "M",
                Gender.FEMALE: "F",
                Gender.OTHER: "N"
            }.get(gender)
            
            # Ищем точное совпадение по всем параметрам
            for employee in bitrix_employees:
                # Проверяем пол, если он указан в Bitrix24
                if bitrix_gender and employee.get('gender') and employee['gender'] != bitrix_gender:
                    continue
                    
                # Проверяем дату рождения, если она указана в Bitrix24
                if employee.get('birth_date'):
                    try:
                        bitrix_birth_date = datetime.strptime(employee['birth_date'], '%Y-%m-%d')
                        if bitrix_birth_date.date() != birth_date.date():
                            continue
                    except (ValueError, TypeError):
                        # Если не удалось распарсить дату, пропускаем эту проверку
                        pass
                
                # Если дошли до этой точки, значит нашли совпадение
                return employee
            
            return None
            
        except Exception as e:
            print(f"Ошибка при поиске сотрудника в Bitrix24: {str(e)}")
            return None

    async def process_welcome_form(
        self,
        first_name: str,
        last_name: str,
        birth_date: datetime,
        gender: Gender
    ) -> WelcomeForm:
        """Обрабатывает приветственную форму и связывает с сотрудником из Bitrix24"""
        
        form = WelcomeForm(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender
        )
        
        try:
            # Ищем сотрудника в Bitrix24
            matching_employee = await self.find_employee_in_bitrix(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                gender=gender
            )
            
            if matching_employee:
                # Если сотрудник найден, создаем или обновляем запись в БД
                employee = self.db.query(Employee).filter_by(crm_id=matching_employee['id']).first()
                
                if not employee:
                    employee = Employee(
                        crm_id=matching_employee['id'],
                        name=f"{first_name} {last_name}",
                        position=matching_employee.get('position'),
                        department=matching_employee.get('department'),
                        email=matching_employee.get('email'),
                        phone=matching_employee.get('phone'),
                        last_sync=datetime.utcnow()
                    )
                    self.db.add(employee)
                
                # Связываем форму с сотрудником
                form.employee = employee
            
        except Exception as e:
            print(f"Ошибка при обработке формы: {str(e)}")
        
        # Сохраняем форму
        self.db.add(form)
        self.db.commit()
        self.db.refresh(form)
        
        return form

    def get_form_by_id(self, form_id: int) -> Optional[WelcomeForm]:
        """Получает форму по ID"""
        return self.db.query(WelcomeForm).filter_by(id=form_id).first()

    def get_forms_by_employee(self, employee_id: int) -> List[WelcomeForm]:
        """Получает все формы сотрудника"""
        return self.db.query(WelcomeForm).filter_by(employee_id=employee_id).all() 