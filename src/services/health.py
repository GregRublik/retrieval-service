from repositories.qdrant import QdrantRepository


class HealthService:

    def __init__(self, qdrant_repository: QdrantRepository):
        self.qdrant_repository = qdrant_repository

    async def check_qdrant(self) -> bool:
        return await self.qdrant_repository.ping()