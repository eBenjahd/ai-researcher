import httpx
from django.conf import settings


class SearXNGService:

    async def search(self, query):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.SEARXNG_URL}/search",
                params={
                    "q": query,
                    "format": "json",
                },
                timeout=30,
            )

        response.raise_for_status()

        return response.json()