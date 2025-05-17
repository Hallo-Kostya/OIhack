from fastapi import FastAPI
from apis.router import router as main_router
from contextlib import asynccontextmanager
import uvicorn
from apis.search import router as search_router
from database.session import sync_engine
from models import Department, User

@asynccontextmanager
async def lifespan(app: FastAPI):
    deps = [
        Department(name="Разработка", description="Отдел разработки в 'Очень Интересно'"),
        Department(name="Тестирование", description="Отдел Тестирования в 'Очень Интересно'"),
        Department(name="Отдел кадров", description="Отдел кадров в 'Очень Интересно'"),
        ]
    users = [
        User(full_name="Александр", birth_date="2005-11-22", role="HR", department_id=3, email="adsada@gmail.com"),
        User(full_name="Александр", birth_date="2005-11-22", role="HR", department_id=3, email="adsada@gmail.com"),
        User(full_name="Александр", birth_date="2005-11-22", role="HR", department_id=3, email="adsada@gmail.com"),
    ]
    yield #back to work cycle
    #app shutdown
    await sync_engine.dispose()


app = FastAPI(title='Ai corporate chat')
app.include_router(main_router)
app.include_router(search_router)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )   