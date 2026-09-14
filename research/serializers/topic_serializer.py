from rest_framework.serializers import ModelSerializer
from research.models import Topic


class TopicSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = [
            "id",
            "name",
            "description",
        ]
        read_only_fields = [
            "id",
        ]