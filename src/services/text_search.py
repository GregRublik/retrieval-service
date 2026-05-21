from schemas.reranker import Chunk
from schemas.websearch import RawPage, ExtractedDocument
from services.embedding import EmbeddingService
import numpy as np


class TextSearchService:
    """Сервис для поиска более релевантной информации в векторах"""

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
    ):

        query_embedding = await self.embedding_service.embed_query(query)
        chunk_embeddings = await self.embedding_service.embed_queries([i.content for i in chunks])

        return self.search_cosine_similarity(query_embedding, chunk_embeddings, top_k)
