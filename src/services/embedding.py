from fastembed import TextEmbedding
from config import settings


class EmbeddingService:

    def __init__(self):
        self.model = TextEmbedding(
            model_name=settings.vdb.embedding_model
        )

    async def embed_query(self, query: str) -> list[list[float]]:
        embeddings = list(self.model.embed([query]))
        return [embedding.tolist() for embedding in embeddings]

    async def embed_queries(self, queries: list[str]) -> list[list[list[float]]]:
        embeddings = list(self.model.embed(queries))
        return [[embedding.tolist()] for embedding in embeddings]
