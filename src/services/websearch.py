from aiohttp import ClientSession
from schemas.websearch import WebSearchRequest

class WebSearchService:

    def __init__(self, session: ClientSession):
        self.session = session


    async def search(self, payload: WebSearchRequest):
        pass
