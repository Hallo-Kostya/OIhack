from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.apis.websocket import ws_router as websocket_router
from src.apis.calendar import calendar_router as calendar_router
from src.apis.employeelist import list_router
from src.apis.auth import auth_router

app = FastAPI(title='Ai corporate chat')
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(websocket_router, prefix="/api")
app.include_router(calendar_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(list_router, prefix="/api")

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
