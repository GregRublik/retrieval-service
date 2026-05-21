from fastapi import FastAPI
import uvicorn

from config import settings
from api.v1.endpoints import search, health, websearch
from contextlib import asynccontextmanager

from exceptions import APIException
from exception_handlers import api_exception_handler
from playwright.async_api import async_playwright

@asynccontextmanager
async def lifespan(_app: FastAPI):
    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=True
    )

    _app.state.browser = browser

    yield

    # await browser.close()
    await playwright.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(search.router, tags=["search"])
app.include_router(websearch.router, tags=["websearch"])
app.include_router(health.router, tags=["health"])

app.add_exception_handler(APIException, api_exception_handler)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
