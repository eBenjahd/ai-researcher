from rest_framework.serializers import ModelSerializer
from research.models import Source


class SourceSerializer(ModelSerializer):

    class Meta:
        model = Source
        fields = [
            "id",
            "name",
            "url",
            "source_type",
        ]
        read_only_fields = [
            "id",
        ]