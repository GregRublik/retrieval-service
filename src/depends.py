from fastapi import Depends

from services import search, embedding, query
from repositories.qdrant import QdrantRepository


def get_qdrant_repository() -> QdrantRepository:
    return QdrantRepository()

def get_query_service() -> query.QueryService:
    return query.QueryService()

def get_embedding_service():
    return embedding.EmbeddingService()

def get_search_service(
    qdrant_repository: QdrantRepository = Depends(get_qdrant_repository),
    embedding_service: embedding.EmbeddingService = Depends(get_embedding_service),
    query_service: query.QueryService = Depends(get_query_service),
) -> search.SearchService:
    return search.SearchService(
        qdrant_repository, embedding_service, query_service
    )
