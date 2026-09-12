from django.db import models
from .document_model import Document

class Topic(models.Model):
    
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )


class DocumentTopic(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    relevance_score = models.FloatField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["document", "topic"],
                name="unique_document_topic",
            ),
        ]