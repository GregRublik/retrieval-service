from fastapi import Depends

from services import search, embedding, query, assistant
from repositories.qdrant import QdrantRepository
from qdrant_client import AsyncQdrantClient
from config import settings
from langchain_huggingface import HuggingFaceEmbeddings



def get_qdrant_repository() -> QdrantRepository:
    client = AsyncQdrantClient("http://localhost:6333")
    return QdrantRepository(
        client
    )

def get_query_service(
    llm_service: assistant.LLMService
) -> query.QueryService:
    return query.QueryService(
        llm_service
    )

def get_embedding_service():
    model = HuggingFaceEmbeddings(
        model_name=settings.vdb.embedding_model,
        encode_kwargs={
            "device": settings.vdb.device,
            "normalize_embeddings": True,
        }
    )
    return embedding.EmbeddingService(

    )

def get_search_service(
    qdrant_repository: QdrantRepository = Depends(get_qdrant_repository),
    embedding_service: embedding.EmbeddingService = Depends(get_embedding_service),
    query_service: query.QueryService = Depends(get_query_service),
) -> search.SearchService:
    return search.SearchService(
        qdrant_repository, embedding_service, query_service
    )
