from typing import List, Optional

from repositories.qdrant import QdrantRepository
from services.embedding import EmbeddingService
from services.query import QueryService

from schemas.search import SearchRequest, SearchResponse, VectorSearchRequest

class SearchService:

    def __init__(
        self,
        qdrant_repository: QdrantRepository,
        embedding_service: EmbeddingService,
        query_service: QueryService,
    ):
        self.qdrant_repository = qdrant_repository
        self.embedding_service = embedding_service
        self.query_service = query_service

    async def search(
            self,
            payload: SearchRequest,
    ) -> SearchResponse:

        # 1. Нормализация запроса
        normalized_query = await self.query_service.rewrite(payload.query)

        # 2. Векторизация
        vector = await self.embedding_service.embed_query(normalized_query)

        # 3. поиск
        return await self.qdrant_repository.search(
            VectorSearchRequest(
                vector=vector,
                top_k=payload.top_k,
                filters=payload.filters
            )
        )

    async def search_by_vector(
        self,
        vector: List[float],
        top_k: int,
        filters: Optional[dict] = None,
    ):
        return await self.qdrant_repository.search(
            vector=vector,
            top_k=top_k,
            filters=filters,
        )

    async def hybrid_search(
        self,
        query: str,
        top_k: int,
        alpha: float = 0.5,
    ):
        query = await self.query_service.rewrite(query)

        vector = await self.embedding_service.embed_query(query)

        results = await self.qdrant_repository.hybrid_search(
            query=query,
            vector=vector,
            top_k=top_k,
            alpha=alpha,
        )

        return results

    async def search_with_scope(
        self,
        query: str,
        scope: dict,
        top_k: int = 5,
    ):
        query = await self.query_service.rewrite(query)

        vector = await self.embedding_service.embed_query(query)

        filters = self._build_scope_filter(scope)

        return await self.qdrant_repository.search(
            vector=vector,
            top_k=top_k,
            filters=filters,
        )