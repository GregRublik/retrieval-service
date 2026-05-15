from fastapi import FastAPI
import uvicorn

from config import settings
from api.v1.endpoints import search, health, websearch


app = FastAPI()

app.include_router(search.router, tags=["search"])
app.include_router(health.router, tags=["health"])
app.include_router(websearch.router, tags=["websearch"])

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
