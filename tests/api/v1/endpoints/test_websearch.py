import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from schemas.websearch import ExtractedDocument, WebSearchRequest, WebSearchResponse


class TestWebSearchEndpoint:
    """POST /web/search — web search"""

    @pytest.fixture
    def app(self, mock_websearch_service):
        from api.v1.endpoints import websearch
        from depends import get_websearch_service
        from exceptions import APIException
        from exception_handlers import api_exception_handler

        app = FastAPI()
        app.include_router(websearch.router)
        app.add_exception_handler(APIException, api_exception_handler)
        app.dependency_overrides[get_websearch_service] = lambda: mock_websearch_service
        return app

    @pytest.fixture
    def client(self, app):
        with TestClient(app) as c:
            yield c

    @pytest.fixture
    def mock_websearch_service(self):
        from services.websearch import WebSearchService

        return AsyncMock(spec=WebSearchService)

    def test_success(self, client, mock_websearch_service):
        mock_websearch_service.process.return_value = WebSearchResponse(
            data=[
                ExtractedDocument(
                    url="https://example.com/1",
                    title="Result 1",
                    content="Content of result 1",
                    score=0.95,
                ),
                ExtractedDocument(
                    url="https://example.com/2",
                    title="Result 2",
                    content="Content of result 2",
                    score=0.85,
                ),
            ]
        )

        payload = {"query": "test query", "top_k": 5}

        response = client.post("/web/search", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["data"]) == 2
        assert data["data"]["data"][0]["url"] == "https://example.com/1"
        assert data["data"]["data"][0]["score"] == 0.95
        assert data["data"]["data"][1]["url"] == "https://example.com/2"
        assert data["data"]["data"][1]["score"] == 0.85

        mock_websearch_service.process.assert_awaited_once_with(WebSearchRequest(**payload))

    def test_empty_results(self, client, mock_websearch_service):
        mock_websearch_service.process.return_value = WebSearchResponse(data=[])

        response = client.post("/web/search", json={"query": "empty query", "top_k": 5})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["data"] == []

    def test_missing_query(self, client):
        response = client.post("/web/search", json={"top_k": 5})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "query" in str(data)

    def test_missing_top_k(self, client):
        response = client.post("/web/search", json={"query": "test"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "top_k" in str(data)

    def test_empty_body(self, client):
        response = client.post("/web/search", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_query_string(self, client, mock_websearch_service):
        mock_websearch_service.process.return_value = WebSearchResponse(data=[])

        response = client.post("/web/search", json={"query": "", "top_k": 5})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["success"] is True

