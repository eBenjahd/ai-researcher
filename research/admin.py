from django.contrib import admin
from research.models import (
    Topic,
    Claim,
    Document,
    DocumentTopic,
    Source,
    Research,
    ResearchDocument,
    DocumentChunk
)

admin.site.register(Topic)
admin.site.register(Claim)
admin.site.register(Document)
admin.site.register(DocumentTopic)
admin.site.register(Source)
admin.site.register(Research)
admin.site.register(ResearchDocument)
admin.site.register(DocumentChunk)