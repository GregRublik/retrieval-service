from fastapi import Depends

from services import search, embedding, query, assistant
from repositories.qdrant import QdrantRepository
from qdrant_client import AsyncQdrantClient
from config import settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings


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
