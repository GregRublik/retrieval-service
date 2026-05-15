from typing import List
from aiohttp import ClientSession
import asyncio

from schemas.fetch import RawPage

class FetchService:
    def __init__(self, session: ClientSession):
        self.session = session

    async def fetch_one(self, url: str) -> str:
            r = await self.session.get(url, follow_redirects=True)
            r.raise_for_status()
            return await r.text()

    async def fetch_all(self, urls: List[str]) -> List[RawPage]:
        tasks = [self.fetch_one(url) for url in urls]
        html_pages = await asyncio.gather(*tasks)

        return [
            RawPage(url=url, html=html)
            for url, html in zip(urls, html_pages)
            if html
        ]