from fastapi import Depends, Request

from repositories.qdrant import QdrantRepository
from repositories.searxng import SearxngRepository
from qdrant_client import AsyncQdrantClient
from aiohttp import ClientSession

from services.text_search import TextSearchService
from utils.session_manager import SessionManager
from config import settings
from services import search, embedding, query, websearch, fetcher, extractor
from services.health import HealthService
from playwright.async_api import Browser


def get_http_session(
        http_session: ClientSession = Depends(SessionManager.get_session),
) -> ClientSession:
    return http_session

def get_qdrant_repository() -> QdrantRepository:
    client = AsyncQdrantClient("http://localhost:6333")
    return QdrantRepository(
        client
    )

def get_query_service() -> query.QueryService:
    return query.QueryService()

def get_embedding_service(
):
    return embedding.EmbeddingService(
    )

def get_textsearch_service(
    embedding_service: embedding.EmbeddingService = Depends(get_embedding_service),
):
    return TextSearchService(embedding_service)

def get_search_service(
    qdrant_repository: QdrantRepository = Depends(get_qdrant_repository),
    embedding_service: embedding.EmbeddingService = Depends(get_embedding_service),
    query_service: query.QueryService = Depends(get_query_service),
    text_search_service: TextSearchService = Depends(get_textsearch_service),
) -> search.SearchService:
    return search.SearchService(
        qdrant_repository, embedding_service, query_service, text_search_service
    )

def get_browser(request: Request):
    return request.app.state.browser

async def get_fetch_service(
        browser: Browser = Depends(get_browser),
):
    return fetcher.FetchService(browser)


def get_extract_service():
    return extractor.ExtractService()


def get_searxng_repository(
    session: ClientSession = Depends(get_http_session),
) -> SearxngRepository:
    return SearxngRepository(
        session=session,
        host=settings.searxng.host,
        port=settings.searxng.port,
    )


def get_health_service(
    qdrant_repository: QdrantRepository = Depends(get_qdrant_repository),
    searxng_repository: SearxngRepository = Depends(get_searxng_repository),
) -> HealthService:
    return HealthService(qdrant_repository, searxng_repository)


def get_websearch_service(
    session: ClientSession = Depends(get_http_session),
    fetcher_service: fetcher.FetchService = Depends(get_fetch_service),
    extractor_service: extractor.ExtractService = Depends(get_extract_service),
    text_search_service: TextSearchService = Depends(get_textsearch_service),
) -> websearch.WebSearchService:
    return websearch.WebSearchService(
        session,
        fetcher=fetcher_service,
        extractor=extractor_service,
        text_search=text_search_service,
    )
