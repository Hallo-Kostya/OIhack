from typing import List
from gigachat import GigaChat as GigaChatSDK
from langchain_gigachat.chat_models import GigaChat
from sqlalchemy import select
from config import settings 
from database.session import async_session_factory,session_factory
from models import User, Event
from fastapi import HTTPException
from datetime import datetime
from langgraph.checkpoint.memory import MemorySaver
from langchain_gigachat.tools.giga_tool import giga_tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


def create_langchain_gigachat() -> GigaChat:
    return GigaChat(
        credentials=settings.GIGACHAT_API_KEY,
        verify_ssl_certs=False
    )


few_shot_examples = [
    {"request": "Выведи все задачи, созданные пользователем с 3 айди", "params":{"user_id": 3}},
]

@giga_tool(few_shot_examples=few_shot_examples)
def get_tasks_for_user(user_id: int) -> List[Event]:
    """
    выводит все события\задачи для пользователя по айди.
    """
    query = select(Event).filter(Event.organizer_id == user_id)
    with session_factory() as session:
        res = session.scalars(query).all()
        return [str(e) for e in res]


async def get_user_by_id(user_id:int) -> User:
    async with async_session_factory() as session:
        query = select(User).filter(User.id == user_id)
        res = await session.scalar(query)
        if res is None:
            raise HTTPException(status_code=404, detail={"error": "User with this id is not found"})
        return res


def analyze_query(query:str):
    print(get_tasks_for_user({"user_id":3}))
    giga = create_langchain_gigachat()
    config = {"configurable": {"thread_id": "id_1"}}
    functions = [get_tasks_for_user]
    giga_with_functions = giga.bind_functions(functions)
    agent_executor = create_react_agent(giga_with_functions, 
                                        functions, 
                                        checkpointer=MemorySaver(),
                                        state_modifier="""Ты бот для помощи сотрудникам, запускай функции с переданными аргументами. Ответ возвращай без отступов, прям то, что возвращает функция и возвращай""")
    resp = agent_executor.invoke({"messages": [HumanMessage(content=query)]}, config=config)
    return resp['messages'][-1].content


async def add_task_for_user(user_id: int, task_name: str, start_time: datetime | None, end_time: datetime | None) -> Event:
    task = Event(organizer_id = user_id, title = task_name, start_time = start_time, end_time = end_time)
    async with async_session_factory() as session:
        session.add(task)
        await session.commit()
    return task
