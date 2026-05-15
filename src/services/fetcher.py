from typing import List
from aiohttp import ClientSession
import asyncio

from schemas.websearch import RawPage

class FetchService:
    def __init__(self, session: ClientSession):
        self.session = session

    async def fetch_one(self, url: str) -> RawPage:
        """Fetch (получить) данные с web страницы"""
        r = await self.session.get(url)
        r.raise_for_status()
        html = await r.text()

        return RawPage(url=url, html=html)

    async def fetch_all(self, urls: List[str]) -> List[RawPage]:
        """Fetch list data from urls"""
        tasks = [self.fetch_one(url) for url in urls]
        raw_pages = await asyncio.gather(*tasks)

        return raw_pages
