from pgvector.django import CosineDistance

from research.models import DocumentChunk

from asgiref.sync import sync_to_async

class RetrievalService:

    def __init__(self, client):

        self.client = client

    async def retrieve(self, query, limit = 10):

        query_embedding = self.client.generate_embedding(
            query
        )

        chunks = await sync_to_async(list)(
            DocumentChunk.objects.annotate(
                distance=CosineDistance(
                    "embedding",
                    query_embedding,
                )
            )
            .order_by("distance")[:limit]
        )
        return chunks

