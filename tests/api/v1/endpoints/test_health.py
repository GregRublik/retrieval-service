from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from services.health import HealthService


@pytest.fixture
def mock_health_service():
    return AsyncMock(spec=HealthService)


@pytest.fixture
def app(mock_health_service):
    from api.v1.endpoints import health
    from depends import get_health_service

    app = FastAPI()
    app.include_router(health.router)
    app.dependency_overrides[get_health_service] = lambda: mock_health_service
    return app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


class TestReadinessEndpoint:

    def test_all_healthy(self, client, mock_health_service):
        mock_health_service.check_qdrant.return_value = True
        mock_health_service.check_searxng.return_value = True

        response = client.get("/ready/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "ready"
        assert len(data["data"]["dependencies"]) == 2
        assert data["data"]["dependencies"][0] == {"name": "qdrant", "healthy": True}
        assert data["data"]["dependencies"][1] == {"name": "searxng", "healthy": True}

        mock_health_service.check_qdrant.assert_awaited_once()
        mock_health_service.check_searxng.assert_awaited_once()

    def test_qdrant_degraded(self, client, mock_health_service):
        mock_health_service.check_qdrant.return_value = False
        mock_health_service.check_searxng.return_value = True

        response = client.get("/ready/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["status"] == "degraded"
        assert data["data"]["dependencies"] == [
            {"name": "qdrant", "healthy": False},
            {"name": "searxng", "healthy": True},
        ]

    def test_searxng_degraded(self, client, mock_health_service):
        mock_health_service.check_qdrant.return_value = True
        mock_health_service.check_searxng.return_value = False

        response = client.get("/ready/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["status"] == "degraded"

    def test_both_degraded(self, client, mock_health_service):
        mock_health_service.check_qdrant.return_value = False
        mock_health_service.check_searxng.return_value = False

        response = client.get("/ready/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["status"] == "degraded"
