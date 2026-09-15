from django.db import models
from .document_model import Document

# Represents a research process focused on answering a specific question.
# A research coordinates the collection and analysis of relevant documents
# and tracks the overall state of the research pipeline.

class Research(models.Model):

    question = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=[
            ("pending", "Pending"),
            ("running", "Running"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )


class ResearchDocument(models.Model):
    research = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
        related_name="research_documents",
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="researches",
    )

    relevance_score = models.FloatField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["research", "document"],
                name="unique_research_document",
            ),
        ]