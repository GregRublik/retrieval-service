from langchain_core.embeddings import Embeddings

class EmbeddingService:

    def __init__(self, model: Embeddings):
        self.model = model

    def get_embedding(self) -> Embeddings:
        return self.model

    async def embed_query(self, query: str) -> list[list[float]]:
        return await self.model.aembed_documents([query])
