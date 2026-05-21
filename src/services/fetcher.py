from typing import List
import asyncio

from playwright.async_api import Browser

from schemas.websearch import RawPage, ResultWebSearch


class FetchService:
    def __init__(self, browser: Browser):
        self.browser = browser

    async def _fetch_one(self, link: ResultWebSearch) -> RawPage:
        """Получить HTML страницы через Playwright"""

        page = await self.browser.new_page()

        try:
            await page.goto(
                link.url,
                timeout=30_000,
                wait_until="domcontentloaded",
            )

            html = await page.content()

            return RawPage(
                url=link.url,
                html=html,
                score=link.score,
                title=link.content,
            )

        finally:
            await page.close()

    async def fetch_all(
        self,
        list_links: List[ResultWebSearch]
    ) -> List[RawPage]:
        """Fetch list data from urls"""
        tasks = [
            self._fetch_one(link)
            for link in list_links
        ]
        return await asyncio.gather(*tasks)
