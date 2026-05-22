import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


@pytest.fixture
def app(mock_search_service):
    from api.v1.endpoints import search
    from depends import get_search_service
    from exceptions import APIException
    from exception_handlers import api_exception_handler

    app = FastAPI()
    app.include_router(search.router)
    app.add_exception_handler(APIException, api_exception_handler)
    app.dependency_overrides[get_search_service] = lambda: mock_search_service
    return app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_search_service():
    from services.search import SearchService

    return AsyncMock(spec=SearchService)
