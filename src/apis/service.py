from typing import List
from gigachat import GigaChat as GigaChatSDK
from langchain_gigachat.chat_models import GigaChat
from sqlalchemy import select
from src.config import settings 
from src.database.session import async_session_factory,session_factory
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from src.session_manager import session_manager

def create_langchain_gigachat() -> GigaChat:
    return GigaChat(
        credentials=settings.GIGACHAT_AUTH_KEY,
        verify_ssl_certs=False
    )

def analyze_query(query:str, user_id:int):
    session = session_manager.get_session(user_id)
    
    agent_executor, thread_id = session.get('agent_executor'), session.get('thread_id')
    config = {"configurable": {"thread_id": thread_id}}
    print(agent_executor)
    resp = agent_executor.invoke({"messages": [HumanMessage(content=query)]}, config=config)
    return resp['messages'][-1].content