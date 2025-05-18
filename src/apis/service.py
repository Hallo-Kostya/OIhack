from typing import List
from gigachat import GigaChat as GigaChatSDK
from langchain_gigachat.chat_models import GigaChat
from sqlalchemy import select
from src.config import settings 
from src.database.session import async_session_factory,session_factory
from src.models import User, Event
from fastapi import HTTPException
from datetime import datetime
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


def create_langchain_gigachat() -> GigaChat:
    return GigaChat(
        credentials=settings.GIGACHAT_AUTH_KEY,
        verify_ssl_certs=False
    )

def analyze_query(query:str):
    giga = create_langchain_gigachat()
    config = {"configurable": {"thread_id": "id_1"}}
    functions = []
    giga_with_functions = giga.bind_functions(functions)
    agent_executor = create_react_agent(giga_with_functions, 
                                        functions, 
                                        checkpointer=MemorySaver(),
                                        state_modifier="""Ты бот для помощи сотрудникам, запускай функции с переданными аргументами. Ответ возвращай без отступов, прям то, что возвращает функция и возвращай. Если ответ пустой, то значит ничего в базе не найдено, так и отвечай, что не найдено""")
    resp = agent_executor.invoke({"messages": [HumanMessage(content=query)]}, config=config)
    return resp['messages'][-1].content
