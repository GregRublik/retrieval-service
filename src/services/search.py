from typing import List, Optional
from qdrant_client.http.exceptions import UnexpectedResponse

from repositories.qdrant import QdrantRepository
from services.embedding import EmbeddingService
from services.query import QueryService

from schemas.search import SearchRequest, SearchResponse, VectorSearchRequest, SearchResult
from exceptions import QdrantCollectionNotFoundException


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

    @staticmethod
    def _is_collection_not_found(error: UnexpectedResponse) -> bool:
        content = error.content.decode() if isinstance(error.content, bytes) else str(error.content)
        return "doesn't exist" in content

    async def search(
            self,
            payload: SearchRequest,
    ) -> SearchResponse:
        try:


            normalized_query = await self.query_service.rewrite(payload.query, rephrase=False)
            vector = await self.embedding_service.embed_query(normalized_query)
            results = await self.qdrant_repository.search(
                VectorSearchRequest(
                    vector=vector[0],
                    top_k=payload.top_k,
                    filters=payload.filters,
                    collection=payload.collection
                )
            )

            return SearchResponse(
                results=[
                    SearchResult(
                        id=point.id,
                        score=point.score,
                        content=point.payload,
                        metadata=point.payload.get("metadata")
                    ) for point in results.points
                ]
            )
        except UnexpectedResponse as e:
            if self._is_collection_not_found(e):
                raise QdrantCollectionNotFoundException
            raise

    async def search_by_vector(
        self,
        payload: VectorSearchRequest,
    ) -> SearchResponse:
        try:
            results = await self.qdrant_repository.search(
                payload,
            )
        except UnexpectedResponse as e:
            if self._is_collection_not_found(e):
                raise QdrantCollectionNotFoundException
            raise

        return SearchResponse(
            results=[
                SearchResult(
                    id=point.id,
                    score=point.score,
                    content=str(point.payload.get("text")),
                    metadata=point.payload.get("metadata")
                ) for point in results.points
            ]
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