from django.db import models

class Source(models.Model):

    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    source_type = models.CharField(
        max_length=50,
        choices=[
            ("news", "News"),
            ("paper", "Paper"),
            ("report", "Report"),
            ("official", "Official"),
        ],
    )