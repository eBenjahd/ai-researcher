from django.db import models
from .document_model import Document

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