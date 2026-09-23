import httpx
from bs4 import BeautifulSoup


class WebPageService:

    async def fetch(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        soup = BeautifulSoup(response.text, "lxml")

        return soup