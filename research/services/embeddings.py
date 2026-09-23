from django.conf import settings

from .providers.openai import OpenAIService


openai_service = OpenAIService(
    api_key=settings.OPENAI_API_KEY,
    model="text-embedding-3-small",
)


def generate_embedding(text: str) -> list[float]:
    return openai_service.generate_embedding(text)