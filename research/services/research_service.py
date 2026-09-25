from asgiref.sync import sync_to_async

from .create_document_chunk import create_document_chunks
from .embedding_chuncks_service import embed_document_chunk


class ResearchService:

    def __init__(
        self,
        relevance_service,
        web_page_service,
        html_extractor,
        document_model,
        source_model,
    ):
        self.relevance_service = relevance_service
        self.web_page_service = web_page_service
        self.html_extractor = html_extractor
        self.document_model = document_model
        self.source_model = source_model

    async def run(self, query):

        relevant_results = (
            await self.relevance_service
            .select_relevant_documents(query)
        )

        if not relevant_results:

            return {
                "status": "no_results",
                "message": (
                    "I couldn't find any search results for this research query. "
                    "The search service may be temporarily unavailable. "
                    "Please try again later."
                ),
                "documents": [],
            }

        documents = []

        for result in relevant_results:

            try:
                html = await self.web_page_service.fetch(
                    result["url"]
                )

                text = self.html_extractor.extract(html)

                source, _ = await sync_to_async(
                    self.source_model.objects.get_or_create
                )(
                    url=result["url"],
                    defaults={
                        "name": result["title"],
                        "source_type": "official",
                    },
                )


                document, created = await sync_to_async(
                    self.document_model.objects.get_or_create
                )(
                    url=result["url"],
                    defaults={
                        "source": source,
                        "title": result["title"],
                        "content": text,
                    },
                )

                if created:

                    chunks = await sync_to_async(
                        create_document_chunks
                    )(document)

                    for chunk in chunks:
                        await sync_to_async(
                            embed_document_chunk
                        )(chunk)

                documents.append({
                    "id": document.id,
                    "title": document.title,
                    "url": document.url,
                })

            except Exception as exc:
                print(
                    f"Failed to process "
                    f"{result['url']}: {exc}"
                    f"{type(exc).__name__}: {exc}"
                )

        return documents