import requests
from config import settings 
from langchain_gigachat.tools.giga_tool import giga_tool

BITRIX_URL=settings.BITRIX_URL

few_shot_examples = [
    {"request": "Верни профиль пользователя Александр Колмаков", "params":{"name": "Александр", "lastname": "Колмаков"}},
    {"request": "Покажи-ка данные пользователя с айди 2 имя по-моему у него Александр", "params":{"id": 2}}
    ]
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
    Получить список сотрудников с их данными. Либо получить конкретного сотрудника если хотя бы один из аргументов передан

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
    return f'{data['NAME']} {data['LASTNAME']} {data['EMAIL']} {data['USER_TYPE']}'