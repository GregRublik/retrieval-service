from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from aiohttp import ClientSession

from services.fetcher import FetchService
from services.extractor import ExtractService
from schemas.websearch import WebSearchResponse, WebSearchRequest, ResultWebSearch


from config import settings
from services.text_search import TextSearchService


class WebSearchService:

    def __init__(
        self,
        session: ClientSession,
        fetcher: FetchService,
        extractor: ExtractService,
        text_search: TextSearchService,
    ):
        self.session = session
        self.fetcher = fetcher
        self.extractor = extractor
        self.text_search = text_search
        self.chunker = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200,
        )

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
        # 1. search urls
        search_results = await self.get_urls(payload.query)
        # 2. fetch pages
        pages = await self.fetcher.fetch_all(search_results)
        # 3. extract text
        documents = [
            self.extractor.extract(page)
            for page in pages
        ]

        return WebSearchResponse(
            data=documents
        )
