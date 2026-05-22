import pytest
from fastapi import status

from exceptions import QdrantCollectionNotFoundException


class TestSearchEndpoint:
    """POST /search/ — text search"""

    def test_success(self, client, mock_search_service):
        mock_search_service.search.return_value = {
            "results": [
                {"id": 1, "score": 0.95, "content": {"text": "doc1"}, "metadata": {"source": "web"}},
                {"id": 2, "score": 0.85, "content": {"text": "doc2"}, "metadata": {"source": "web"}},
            ]
        }

        payload = {
            "query": "test query",
            "top_k": 5,
            "collection": "my_collection",
        }

        response = client.post("/search/query/", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["results"]) == 2
        assert data["data"]["results"][0]["score"] == 0.95

        mock_search_service.search.assert_awaited_once()

    def test_collection_not_found(self, client, mock_search_service):
        mock_search_service.search.side_effect = QdrantCollectionNotFoundException()

        payload = {
            "query": "test",
            "collection": "nonexistent",
        }

        response = client.post("/search/query/", json=payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Collection not found exception"

    def test_accepts_filters(self, client, mock_search_service):
        mock_search_service.search.return_value = {"results": []}

        payload = {
            "query": "filtered search",
            "collection": "my_collection",
            "filters": {"source": "news"},
        }

        response = client.post("/search/query/", json=payload)

        assert response.status_code == status.HTTP_200_OK
        call_args, _ = mock_search_service.search.await_args
        assert call_args[0].filters == {"source": "news"}

    def test_default_top_k(self, client, mock_search_service):
        mock_search_service.search.return_value = {"results": []}

        payload = {
            "query": "default top_k",
            "collection": "my_collection",
        }

        response = client.post("/search/query/", json=payload)

        assert response.status_code == status.HTTP_200_OK
        call_args, _ = mock_search_service.search.await_args
        assert call_args[0].top_k == 5


class TestSemanticSearchInTextsEndpoint:
    """POST /search/semantic_in_texts/ — search within provided documents"""

    def test_success(self, client, mock_search_service):
        mock_search_service.search_by_query_in_text.return_value = {
            "results": [
                {"url": "https://example.com/1", "title": "Doc 1", "content": "content 1", "score": 0.92},
                {"url": "https://example.com/2", "title": "Doc 2", "content": "content 2", "score": 0.78},
            ]
        }

        payload = {
            "query": "find relevant",
            "documents": [
                {"url": "https://example.com/1", "title": "Doc 1", "content": "content 1", "score": 0.5},
                {"url": "https://example.com/2", "title": "Doc 2", "content": "content 2", "score": 0.3},
            ],
            "top_k": 3,
        }

        response = client.post("/search/semantic_in_texts/", json=payload)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["results"]) == 2
        assert data["data"]["results"][0]["score"] == 0.92

        mock_search_service.search_by_query_in_text.assert_awaited_once()

    def test_default_top_k(self, client, mock_search_service):
        mock_search_service.search_by_query_in_text.return_value = {"results": []}

        payload = {
            "query": "find",
            "documents": [
                {"url": "https://example.com/1", "title": "Doc 1", "content": "content", "score": 0.5},
            ],
        }

        response = client.post("/search/semantic_in_texts/", json=payload)

        assert response.status_code == status.HTTP_200_OK
        call_args, _ = mock_search_service.search_by_query_in_text.await_args
        assert call_args[0].top_k == 5

    def test_empty_documents(self, client, mock_search_service):
        mock_search_service.search_by_query_in_text.return_value = {"results": []}

        payload = {
            "query": "find",
            "documents": [],
            "top_k": 5,
        }

        response = client.post("/search/semantic_in_texts/", json=payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["results"] == []


class TestSearchByVectorEndpoint:
    """GET /search/vector/ — search by vector embedding"""

    def test_success(self, client, mock_search_service):
        mock_search_service.search_by_vector.return_value = {
            "results": [
                {"id": 1, "score": 0.99, "content": {"text": "some text"}, "metadata": {"source": "pdf"}},
            ]
        }

        response = client.post(
            "/search/vector/",
            json={
                "collection": "my_collection",
                "top_k": 5,
                "vector": [0.1, 0.2, 0.3, 0.4],
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["results"]) == 1
        assert data["data"]["results"][0]["score"] == 0.99

        mock_search_service.search_by_vector.assert_awaited_once()

    def test_collection_not_found(self, client, mock_search_service):
        mock_search_service.search_by_vector.side_effect = QdrantCollectionNotFoundException()

        response = client.post(
            "/search/vector/",
            json={
                "collection": "nonexistent",
                "vector": [0.1, 0.2, 0.3],
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Collection not found exception"

    def test_default_top_k(self, client, mock_search_service):
        mock_search_service.search_by_vector.return_value = {"results": []}

        response = client.post(
            "/search/vector/",
            json={
                "collection": "my_collection",
                "vector": [0.1, 0.2, 0.3],
            },
        )

        assert response.status_code == status.HTTP_200_OK
        call_args, _ = mock_search_service.search_by_vector.await_args
        assert call_args[0].top_k == 5


class TestStubEndpoints:
    """Stub endpoints that are not yet implemented"""

    def test_hybrid_search_stub(self, client):
        response = client.post("/search/hybrid/")
        assert response.status_code == status.HTTP_200_OK

    def test_search_with_scope_stub(self, client):
        response = client.get("/search/with_scope/")
        assert response.status_code == status.HTTP_200_OK
