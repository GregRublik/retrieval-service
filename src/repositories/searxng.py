from aiohttp import ClientSession

from config import settings


class SearxngRepository:

    def __init__(self, session: ClientSession, host: str, port: int):
        self.session = session
        self.host = host
        self.port = port

    async def ping(self) -> bool:
        try:
            url = f"http://{self.host}:{self.port}/search?q=test&format=json"
            response = await self.session.get(url)
            return response.status == 200
        except Exception:
            return False