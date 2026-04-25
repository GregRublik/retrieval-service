from fastapi import FastAPI
import uvicorn

from config import settings
from api.v1.endpoints import query, search


app = FastAPI()

app.include_router(search.router)
app.include_router(query.router)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
