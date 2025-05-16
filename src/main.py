from fastapi import FastAPI
from apis.router import router as main_router
import uvicorn
from apis.search import router as search_router

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