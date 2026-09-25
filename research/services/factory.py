from django.conf import settings

from research.models import Document, Source

from .research_service import ResearchService
from .relevance_service import RelevanceService

from .discovery.web_search_service import WebPageService
from .discovery.html_extractor import HTMLExtractionService

from .providers.jev import JEVService


def build_research_service():

    jev = JEVService(
        api_key=settings.JEV_API_KEY,
        model="jev-1.13.0",
    )

    relevance = RelevanceService(
        provider=jev,
    )

    web_page = WebPageService()
    extractor = HTMLExtractionService()

    return ResearchService(
        relevance_service=relevance,
        web_page_service=web_page,
        html_extractor=extractor,
        document_model=Document,
        source_model=Source,
    )