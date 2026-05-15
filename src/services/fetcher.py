from typing import List
from aiohttp import ClientSession
import asyncio

from schemas.websearch import RawPage, ResultWebSearch

class FetchService:
    def __init__(self, session: ClientSession):
        self.session = session

    async def fetch_one(self, link: ResultWebSearch) -> RawPage:
        """Fetch (получить) данные с web страницы"""
        r = await self.session.get(link.url)
        r.raise_for_status()
        html = await r.text()
        return RawPage(url=link.url, html=html, score=link.score, title=link.content)

    async def fetch_all(self, list_links: List[ResultWebSearch]) -> List[RawPage]:
        """Fetch list data from urls"""
        tasks = [self.fetch_one(link) for link in list_links]
        raw_pages = await asyncio.gather(*tasks)

        return raw_pages
