from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Dict, List
from src.apis.service import analyze_query
import json
import logging
import asyncio
from src.session_manager import session_manager
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ws_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int,WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        session_manager.create_session(user_id)    
        logger.info(f"Новое подключение. Всего активных соединений: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, user_id:int):
        if user_id in self.active_connections:
            self.active_connections.pop(user_id)
            session_manager.remove_session(user_id)
            logger.info(f"Соединение заremoveкрыто. Осталось активных соединений: {len(self.active_connections)}")

    async def send_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
            logger.debug("Сообщение отправлено")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {str(e)}")

    async def process_message(self, user_id:int, message: str, websocket: WebSocket):
        try:
            loop = asyncio.get_event_loop()
            ai_response = await loop.run_in_executor(
                None, 
                lambda: analyze_query(message, user_id) 
            )
            websocket = self.active_connections.get(user_id, None)
            if websocket:
                await self.send_message(
                    json.dumps({
                        "type": "response",
                        "message": ai_response
                    }, ensure_ascii=False),
                    websocket
                )
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {str(e)}")
            await self.send_message(
                json.dumps({
                    "type": "error",
                    "message": "Произошла ошибка при обработке сообщения"
                }),
                websocket
            )

manager = ConnectionManager()

@ws_router.websocket("/ws/chat/")
async def websocket_endpoint(websocket: WebSocket):
    query_params = websocket.query_params
    user_id = int(query_params.get('user_id', None))
    if user_id is not None:
        await manager.connect(websocket, user_id)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                try:
                    message_data = json.loads(data)
                    user_message = message_data.get('message', '')
                    if user_message:
                        await manager.process_message(user_id, user_message, websocket)
                except json.JSONDecodeError:
                    logger.error("Неверный формат JSON")
                    await manager.send_message(
                        json.dumps({
                            "type": "error",
                            "message": "Неверный формат сообщения"
                        }),
                        websocket
                    )
            except WebSocketDisconnect:
                logger.info("Клиент закрыл соединение")
                break
            except Exception as e:
                logger.error(f"Ошибка в цикле обработки: {str(e)}")
                break
    except Exception as e:
        logger.error(f"Критическая ошибка WebSocket: {str(e)}")
    finally:
        manager.disconnect(websocket, user_id)