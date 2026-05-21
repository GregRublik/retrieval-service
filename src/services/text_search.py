from schemas.websearch import ExtractedDocument
from schemas.search import SearchQueryTextResponse

from services.embedding import EmbeddingService
import numpy as np


class TextSearchService:
    """Сервис для поиска более релевантной информации в текстах"""

    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    @staticmethod
    def cosine_similarity(a, b):
        a = np.asarray(a).reshape(-1)
        b = np.asarray(b).reshape(-1)

        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search_cosine_similarity(self, query_vector, vectors, top_k=5):
        scores = [
            (i, self.cosine_similarity(query_vector, v))
            for i, v in enumerate(vectors)
        ]

        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_k]

    async def retrieve(
        self,
        query: str,
        chunks: list[ExtractedDocument],
        top_k: int = 5
    ) -> SearchQueryTextResponse:

        query_embedding = await self.embedding_service.embed_query(query)

        chunk_embeddings = await self.embedding_service.embed_queries(
            [i.content for i in chunks]
        )

        results = self.search_cosine_similarity(
            query_embedding,
            chunk_embeddings,
            top_k
        )

        documents = []

        for index, score in results:
            doc = chunks[index]

            documents.append(
                ExtractedDocument(
                    url=doc.url,
                    title=doc.title,
                    content=doc.content,
                    score=float(score),
                )
            )

        return SearchQueryTextResponse(
            results=documents
        )