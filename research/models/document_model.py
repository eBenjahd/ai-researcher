from django.db import models
from .source_model import Source

class Document(models.Model):
    
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    content = models.TextField()

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    summary = models.TextField(
        blank=True,
    )

    language = models.CharField(
        max_length=10,
        default="en",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )