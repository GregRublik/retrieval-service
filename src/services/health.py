from repositories.qdrant import QdrantRepository
from repositories.searxng import SearxngRepository


class HealthService:

    def __init__(self, qdrant_repository: QdrantRepository, searxng_repository: SearxngRepository):
        self.qdrant_repository = qdrant_repository
        self.searxng_repository = searxng_repository

    async def check_qdrant(self) -> bool:
        return await self.qdrant_repository.ping()

    async def check_searxng(self) -> bool:
        return await self.searxng_repository.ping()