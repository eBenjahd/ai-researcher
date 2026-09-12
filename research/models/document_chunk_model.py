from django.db import models
from pgvector.django import VectorField
from .document_model import Document


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
    )
    content = models.TextField()
    embedding = VectorField(
        dimensions=1536,
        null=True,
        blank=True,
    )
    chunk_index = models.IntegerField()