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

def get_bitrix_api() -> Bitrix24API:
    """
    Возвращает экземпляр Bitrix24API с настройками из конфигурации.
    Используется как зависимость в FastAPI.
    """
    return Bitrix24API(webhook_url=settings.BITRIX_WEBHOOK_URL)