from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from config import settings

embeddings = HuggingFaceEmbeddings(
    model_name=settings.vdb.embedding_model,
    encode_kwargs={
        "device": settings.vdb.device,
        "normalize_embeddings": True,
    }
)

class EmbeddingService:

    def __init__(self, model: Embeddings):
        self.model = model

    def get_embedding(self) -> Embeddings:
        return self.model

    async def embed_query(self, query: str) -> list[list[float]]:
        return await self.model.aembed_documents([query])

    async def embed_queries(self, queries: list[str]) -> list[list[list[float]]]:
        vectors = []
        for query in queries:
            vectors.append(await self.embed_query(query))
        return vectors