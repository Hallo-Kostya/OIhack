from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.calendar import Employee
from src.apis.bitrix24 import Bitrix24API
from src.config import settings

class CalendarSyncService:
    def __init__(self, bitrix_api: Bitrix24API):
        self.bitrix = bitrix_api

    async def sync_employees(self, session: AsyncSession):
        """
        Синхронизирует информацию о сотрудниках из CRM
        
        Args:
            session: Сессия базы данных
        """
        try:
            # Получаем список сотрудников из CRM
            employees = self.bitrix.get_employees()
            
            if not employees.get('result'):
                return
            
            # Получаем существующих сотрудников
            existing_employees = await session.execute(
                select(Employee)
            )
            existing_employees = {emp.crm_id: emp for emp in existing_employees.scalars().all()}

            current_crm_ids = set()

            for emp in employees['result']:
                crm_id = emp['ID']
                current_crm_ids.add(crm_id)

                if crm_id in existing_employees:
                    # Обновляем существующего сотрудника
                    db_emp = existing_employees[crm_id]
                    db_emp.name = emp['NAME']
                    db_emp.position = emp.get('POSITION', '')
                    db_emp.department = emp.get('DEPARTMENT', '')
                    db_emp.email = emp.get('EMAIL', '')
                    db_emp.phone = emp.get('PHONE', '')
                    db_emp.last_sync = datetime.now()
                else:
                    # Создаем нового сотрудника
                    new_emp = Employee(
                        crm_id=crm_id,
                        name=emp['NAME'],
                        position=emp.get('POSITION', ''),
                        department=emp.get('DEPARTMENT', ''),
                        email=emp.get('EMAIL', ''),
                        phone=emp.get('PHONE', ''),
                        last_sync=datetime.now()
                    )
                    session.add(new_emp)

            # Удаляем сотрудников, которых больше нет в CRM
            for crm_id, db_emp in existing_employees.items():
                if crm_id not in current_crm_ids:
                    await session.delete(db_emp)

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e

    async def get_employees(self, session: AsyncSession):
        """
        Получает список сотрудников из базы данных
        
        Args:
            session: Сессия базы данных
        """
        result = await session.execute(select(Employee))
        return result.scalars().all() 