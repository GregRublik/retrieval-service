from schemas.search import VectorSearchRequest
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client.models import QueryResponse
from config import settings
from schemas.search import SearchResult

class QdrantRepository:

    def __init__(self, client: AsyncQdrantClient) -> None:
        self.client = client

    async def search(self, payload: VectorSearchRequest) -> QueryResponse:

        query_filter = None

        if payload.filters:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                    for key, value in payload.filters.items()
                ]
            )


        points = await self.client.query_points(
            collection_name=payload.collection,
            query=payload.vector,
            query_filter=query_filter,
            with_payload=True,
            limit=10
        )

        # print(type(points))
        return points

        # return SearchResult(
        #     vector_id="1",
        #     score=1,
        #     content="sdf",
        #     metadata={}
        # )
