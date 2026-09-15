from django.db import models
from .document_model import Document

# Represents a specific factual statement extracted from a document.
# Claims are used as evidence-backed facts during the research process,
# allowing the system to trace conclusions and analysis back to their source.

class Claim(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="claims",
    )

    statement = models.TextField()

    confidence_score = models.FloatField(
        null=True,
        blank=True,
    )