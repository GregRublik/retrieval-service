from typing import List, Dict

from services.fetcher import FetchService
from services.extractor import ExtractService
from services.reranker import RerankerService
from schemas.websearch import WebSearchResponse, WebSearchRequest, ResultWebSearch
from aiohttp import ClientSession

from config import settings

from pydantic import BaseModel


class WebSearchService:

    def __init__(self, session: ClientSession, fetcher: FetchService, extractor: ExtractService):
        self.session = session
        self.fetcher = fetcher
        self.extractor = extractor

    async def get_urls(self, query: str) -> List[ResultWebSearch]:
        """Get list links of web search"""
        response = await self.session.get(
            f"http://{settings.searxng.host}:{settings.searxng.port}/search?q={query}&format=json"
        )
        response = await response.json()
        return [
            ResultWebSearch(
                url=data.get("url"),
                title=data.get("title"),
                content=data.get("content"),
                score=data.get("score"),
            ) for data in response.get("results")
        ]

    async def process(self, payload: WebSearchRequest) -> WebSearchResponse:
        """Process web search data from query"""
        search_results = await self.get_urls(payload.query)
        reranked_urls = RerankerService.rerank(search_results, payload.top_k)

        pages = await self.fetcher.fetch_all(reranked_urls)

        return WebSearchResponse(
            data=[
                self.extractor.extract(page)
                for page in pages
            ]
        )

