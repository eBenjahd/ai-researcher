import requests
from django.conf import settings


class SearXNGService:

    def search(self, query):

        response = requests.get(
            f"{settings.SEARXNG_URL}/search",
            params={
                "q": query,
                "format" : "json"
            },
            timeout=30
            )
        
        response.raise_for_status()

        return response.json()