from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from src.apis.service import analyze_query
import json
import logging
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Новое подключение. Всего активных соединений: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Соединение закрыто. Осталось активных соединений: {len(self.active_connections)}")

    async def send_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
            logger.debug("Сообщение отправлено")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {str(e)}")
            self.disconnect(websocket)

    async def process_message(self, message: str, websocket: WebSocket):
        try:
            loop = asyncio.get_event_loop()
            ai_response = await loop.run_in_executor(
                None, 
                lambda: analyze_query(message) 
            )
            
            await self.send_message(
                json.dumps({
                    "type": "response",
                    "message": ai_response
                }),
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

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                try:
                    message_data = json.loads(data)
                    user_message = message_data.get('message', '')
                    if user_message:
                        await manager.process_message(user_message, websocket)
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
        manager.disconnect(websocket)