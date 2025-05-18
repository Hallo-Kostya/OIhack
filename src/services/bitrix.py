import requests
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timedelta
from fastapi import Depends
from src.config import settings

class Bitrix24API:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url.rstrip('/')
        self.base_url = f"{self.webhook_url}/"

    def _make_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполняет запрос к Bitrix24 API"""
        url = f"{self.base_url}{method}"
        response = requests.post(url, json=params or {})
        response.raise_for_status()
        return response.json()

    def get_calendar_events(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Получает события календаря за указанный период"""
        return self._make_request("calendar.event.get", {
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d")
        })

    def get_calendar_sections(self) -> Dict[str, Any]:
        """Получает список календарей пользователя"""
        return self._make_request("calendar.section.get")

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """
        Получает список всех сотрудников из Bitrix24.
        Возвращает список словарей с данными сотрудников.
        """
        try:
            # Получаем всех сотрудников через user.get
            response = self._make_request("user.get", {
                "FILTER": {
                    "ACTIVE": True
                },
                "FIELDS": [
                    "ID",
                    "NAME",
                    "LAST_NAME",
                    "SECOND_NAME",
                    "EMAIL",
                    "PERSONAL_PHONE",
                    "PERSONAL_MOBILE",
                    "WORK_PHONE",
                    "PERSONAL_POSITION",
                    "PERSONAL_GENDER",
                    "PERSONAL_BIRTHDAY",
                    "PERSONAL_PHOTO",
                    "PERSONAL_CITY",
                    "PERSONAL_STREET",
                    "PERSONAL_MAILBOX",
                    "PERSONAL_STATE",
                    "PERSONAL_ZIP",
                    "PERSONAL_COUNTRY",
                    "PERSONAL_PROFESSION",
                    "PERSONAL_WWW",
                    "PERSONAL_ICQ",
                    "PERSONAL_FAX",
                    "PERSONAL_PAGER",
                    "PERSONAL_NOTES",
                    "PERSONAL_MAILBOX",
                    "PERSONAL_CITY",
                    "PERSONAL_STREET",
                    "PERSONAL_STATE",
                    "PERSONAL_ZIP",
                    "PERSONAL_COUNTRY",
                    "WORK_POSITION",
                    "WORK_COMPANY",
                    "WORK_DEPARTMENT",
                    "WORK_PHONE",
                    "WORK_FAX",
                    "WORK_MAILBOX",
                    "WORK_CITY",
                    "WORK_STREET",
                    "WORK_STATE",
                    "WORK_ZIP",
                    "WORK_COUNTRY",
                    "WORK_PROFILE",
                    "WORK_LOGO",
                    "WORK_NOTES",
                    "ADMIN_NOTES",
                    "STORED_HASH",
                    "XML_ID",
                    "PERSONAL_BIRTHDATE",
                    "EXTERNAL_AUTH_ID",
                    "CHECKWORD_TIME",
                    "CONFIRM_CODE",
                    "LOGIN_ATTEMPTS",
                    "LAST_ACTIVITY_DATE",
                    "AUTO_TIME_ZONE",
                    "TIME_ZONE",
                    "TIME_ZONE_OFFSET",
                    "TITLE",
                    "BX_USER_ID",
                    "LANGUAGE_ID",
                    "BLOCKED",
                    "IS_ONLINE",
                    "IS_REAL_USER",
                    "INDEX",
                    "REGISTERED",
                    "PERSONAL_GENDER",
                    "PERSONAL_PROFESSION",
                    "PERSONAL_WWW",
                    "PERSONAL_ICQ",
                    "PERSONAL_FAX",
                    "PERSONAL_PAGER",
                    "PERSONAL_STREET",
                    "PERSONAL_MAILBOX",
                    "PERSONAL_CITY",
                    "PERSONAL_STATE",
                    "PERSONAL_ZIP",
                    "PERSONAL_COUNTRY",
                    "PERSONAL_BIRTHDATE",
                    "PERSONAL_PHOTO",
                    "PERSONAL_NOTES",
                    "WORK_COMPANY",
                    "WORK_DEPARTMENT",
                    "WORK_POSITION",
                    "WORK_WWW",
                    "WORK_PHONE",
                    "WORK_FAX",
                    "WORK_PAGER",
                    "WORK_STREET",
                    "WORK_MAILBOX",
                    "WORK_CITY",
                    "WORK_STATE",
                    "WORK_ZIP",
                    "WORK_COUNTRY",
                    "WORK_PROFILE",
                    "WORK_LOGO",
                    "WORK_NOTES"
                ]
            })

            if not response.get('result'):
                return []

            # Преобразуем ответ в нужный формат
            employees = []
            for user in response['result']:
                employee = {
                    'id': user['ID'],
                    'name': f"{user.get('NAME', '')} {user.get('LAST_NAME', '')}".strip(),
                    'first_name': user.get('NAME', ''),
                    'last_name': user.get('LAST_NAME', ''),
                    'email': user.get('EMAIL', ''),
                    'work_position': user.get('WORK_POSITION', ''),
                    'department': user.get('WORK_DEPARTMENT', ''),
                    'gender': user.get('PERSONAL_GENDER', ''),
                    'birth_date': user.get('PERSONAL_BIRTHDATE', ''),
                    'avatar': user.get('PERSONAL_PHOTO', ''),
                    'phones': {
                        'work_phone': user.get('WORK_PHONE', ''),
                        'personal_mobile': user.get('PERSONAL_MOBILE', ''),
                        'personal_phone': user.get('PERSONAL_PHONE', '')
                    }
                }
                employees.append(employee)

            return employees

        except Exception as e:
            raise Exception(f"Ошибка при получении списка сотрудников: {str(e)}")

def get_bitrix_api() -> Bitrix24API:
    """
    Возвращает экземпляр Bitrix24API с настройками из конфигурации.
    Используется как зависимость в FastAPI.
    """
    return Bitrix24API(webhook_url=settings.BITRIX_WEBHOOK_URL)