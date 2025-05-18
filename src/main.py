from fastapi import FastAPI
from src.apis.router import router as main_router
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.apis.websocket import router as websocket_router
from src.apis.calendar import router as calendar_router

app = FastAPI(title='Ai corporate chat')
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main_router)
app.include_router(websocket_router, prefix="/api")
app.include_router(calendar_router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API работает"}
