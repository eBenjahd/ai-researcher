from rest_framework.serializers import ModelSerializer
from research.models import Research


class ResearchSerializer(ModelSerializer):

    class Meta:
        model = Research
        fields = [
            "id",
            "question",
            "status",
            "created_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "completed_at",
        ]