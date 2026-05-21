from typing import List, Dict

from services.fetcher import FetchService
from services.extractor import ExtractService
from services.reranker import RerankerService
from schemas.websearch import WebSearchResponse, WebSearchRequest, ResultWebSearch
from aiohttp import ClientSession

from config import settings

from pydantic import BaseModel


class WebSearchService:

    def __init__(self, session: ClientSession, fetcher: FetchService, extractor: ExtractService, reranker: RerankerService):
        self.session = session
        self.fetcher = fetcher
        self.extractor = extractor
        self.reranker = RerankerService

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

    async def process(self, payload: WebSearchRequest):
        """Process web search data from query"""
        # 1. search urls
        search_results = await self.get_urls(payload.query)
        # 2. rerank urls
        reranked_urls = self.reranker.rerank(
            search_results,
            payload.top_k
        )
        # 3. fetch pages
        pages = await self.fetcher.fetch_all(reranked_urls)

        # 4. extract text
        documents = [
            self.extractor.extract(page)
            for page in pages
        ]

        # 5. chunking
        chunks = []

        for doc in documents:
            print(doc)
            break
            # parts = self.chunker.split_text(doc.text)
            #
            # for part in parts:
            #     chunks.append(
            #         Chunk(
            #             text=part,
            #             source_url=doc.url,
            #             title=doc.title,
            #         )
            #     )

        # # 6. semantic search
        # relevant_chunks = await self.semantic_search.search(
        #     query=payload.query,
        #     chunks=chunks,
        #     top_k=payload.top_k
        # )

        # return relevant_chunks

        return WebSearchResponse(
            data=documents
        )

