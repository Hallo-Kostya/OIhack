import requests
from sqlalchemy import select
from src.config import settings 
from langchain_gigachat.tools.giga_tool import giga_tool
from src.database.session import session_factory, async_session_factory
from src.models.user import WorkStatus
from datetime import datetime

from src.models.user import User
BITRIX_URL=settings.BITRIX24_WEBHOOK_URL

few_shot_examples = [
    {"request": "Верни профиль пользователя Александр Колмаков", "params":{"name": "Александр", "lastname": "Колмаков"}},
    {"request": "Покажи-ка данные пользователя с айди 2 имя по-моему у него Александр", "params":{"id": 2}}
    ]

def format_users(users: list[dict]) -> list[str]:
    formatted = []
    for user in users:
        name = user.get("NAME", "").strip()
        last_name = user.get("LAST_NAME", "").strip()
        email = user.get("EMAIL", "").strip()
        department_id = user.get("UF_DEPARTMENT", "")
        user_type = user.get("USER_TYPE", "").strip()

        if name or last_name:
            full_name = f"{name} {last_name}".strip()
            formatted.append(f"{full_name} — {email}")
        else:
            formatted.append(f"{email}")
        if department_id:
            formatted.append(f"из отдела с айди {department_id[0]}")
        formatted.append(f"Роль сотрудника: {user_type}")
    return " ".join(formatted)

@giga_tool(few_shot_examples=few_shot_examples)
def get_bitrix_users(
    active: str = None,
    email: str = None,
    name: str = None,
    lastname: str = None,
    id: int = None,
    department_id: int = None,
    admin: str = None,
    sort: str = "ID",
    order: str = "ASC",
) -> list:
    
    """
    Получить список сотрудников из битрикса с их данными. Либо получить конкретного сотрудника если хотя бы один из аргументов передан

    :param active: 'Y' или 'N' — активен ли пользователь
    :param email: фильтр по email
    :param name: фильтр по имени
    :param lastname: фильтр по фамилии
    :param id: конкретный ID пользователя
    :param department_id: ID отдела (для фильтра по отделу)
    :param admin: 'Y' или 'N' — администратор
    :param sort: поле сортировки (например, "ID", "LAST_NAME")
    :param order: порядок сортировки ("ASC" или "DESC")
    :return: список пользователей
    """

    url = f"{BITRIX_URL}/user.get"

    # Сборка фильтров
    filters = {}
    if active:
        filters["ACTIVE"] = active
    if email:
        filters["EMAIL"] = email
    if name:
        filters["NAME"] = name
    if lastname:
        filters["LAST_NAME"] = lastname
    if id:
        filters["ID"] = id
    if department_id:
        filters["UF_DEPARTMENT"] = department_id
    if admin:
        filters["IS_ADMIN"] = admin

    payload = {
        "FILTER": filters,
        "SORT": sort,
        "ORDER": order
    }
    print("🔍 Параметры для Bitrix:", payload)
    response = requests.post(url, json=payload)
    data = response.json()

    if "error" in data:
        raise Exception(f"Bitrix error: {data['error_description']}")
    data = data["result"]
    workers = format_users(data)
    print(workers)
    return workers