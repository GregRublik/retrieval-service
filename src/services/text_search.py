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

        return np.dot(a, b) / (
            np.linalg.norm(a) * np.linalg.norm(b)
        )

    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 1200,
        overlap: int = 250,
    ):
        chunks = []

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start += chunk_size - overlap

        return chunks

    async def retrieve(
        self,
        query: str,
        documents: list[ExtractedDocument],
        top_k: int = 5
    ) -> SearchQueryTextResponse:

        query_embedding = (
            await self.embedding_service.embed_query(query)
        )[0]

        semantic_chunks = []

        for doc in documents:

            text_chunks = self.split_text(doc.content)

            embeddings = await self.embedding_service.embed_queries(
                text_chunks
            )

            for chunk_text, embedding in zip(text_chunks, embeddings):

                score = self.cosine_similarity(
                    query_embedding,
                    embedding
                )

                semantic_chunks.append({
                    "url": doc.url,
                    "title": doc.title,
                    "content": chunk_text,
                    "score": float(score),
                })

        semantic_chunks.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        top_results = semantic_chunks[:top_k]

        return SearchQueryTextResponse(
            results=[
                ExtractedDocument(**item)
                for item in top_results
            ]
        )