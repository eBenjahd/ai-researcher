from rest_framework.serializers import ModelSerializer
from research.models import Claim


class ClaimSerializer(ModelSerializer):

    class Meta:
        model = Claim
        fields = [
            "id",
            "document",
            "statement",
            "confidence_score",
        ]
        read_only_fields = [
            "id",
        ]