import unicodedata
import re

from services.embedding import EmbeddingService
from services.assistant import LLMService



class QueryService:

    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service


    async def rewrite(self, query, rephrase: bool = False) -> str:
        normalized_query = self._normalize_basic(query)

        # query = self._apply_synonyms(normalized_query)
        #
        # query = self._normalize_structure(query)

        if rephrase:
            query = await self._llm_rewrite(query)

        return query

    @staticmethod
    def _normalize_basic(query: str) -> str:
        query = query.strip()
        query = unicodedata.normalize("NFKC", query)
        query = query.lower()
        query = re.sub(r"\s+", " ", query)
        return query

    async def _llm_rewrite(self, query: str) -> str:
        query = self.llm_service.rephrase(query)
        return query
