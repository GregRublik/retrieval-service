from fastapi import Depends


from repositories.qdrant import QdrantRepository
from qdrant_client import AsyncQdrantClient
from langchain_core.embeddings import Embeddings
from aiohttp import ClientSession
from utils.session_manager import SessionManager
from services import search, embedding, query, assistant, websearch, fetcher, extractor, reranker


def get_http_session(
        http_session: ClientSession = Depends(SessionManager.get_session),
) -> ClientSession:
    return http_session


def get_embeddings() -> Embeddings:
    return embedding.embeddings

def get_qdrant_repository() -> QdrantRepository:
    client = AsyncQdrantClient("http://localhost:6333")
    return QdrantRepository(
        client
    )

def get_query_service(
    # llm_service: assistant.LLMService = Depends()
) -> query.QueryService:
    return query.QueryService(
        # llm_service
    )

def get_embedding_service(
    embeddings: Embeddings = Depends(get_embeddings)
):
    return embedding.EmbeddingService(
        model=embeddings,
    )

def get_search_service(
    qdrant_repository: QdrantRepository = Depends(get_qdrant_repository),
    embedding_service: embedding.EmbeddingService = Depends(get_embedding_service),
    query_service: query.QueryService = Depends(get_query_service),
) -> search.SearchService:
    return search.SearchService(
        qdrant_repository, embedding_service, query_service
    )

def get_fetch_service(
    session: ClientSession = Depends(get_http_session),
):
    return fetcher.FetchService(session)

def get_extract_service():
    return extractor.ExtractService()

def get_reranker_service():
    return reranker.RerankerService()

def get_websearch_service(
    session: ClientSession = Depends(get_http_session),
    fetcher_service: fetcher.FetchService = Depends(get_fetch_service),
    extractor_service: extractor.ExtractService = Depends(get_extract_service),
    reranker_service: reranker.RerankerService = Depends(get_reranker_service)
) -> websearch.WebSearchService:
    return websearch.WebSearchService(
        session,
        fetcher=fetcher_service,
        extractor=extractor_service,
        reranker=reranker_service
    )
