from rest_framework.serializers import ModelSerializer
from research.models import Document


class DocumentSerializer(ModelSerializer):

    class Meta: 
        model = Document
        fields = [
            "id", 
            "source",
            "title",
            "url",
            "content",
            "published_at",
            "summary",
            "language",
            "created_at"
        ]
        read_only_fields = ["id","created_at"]