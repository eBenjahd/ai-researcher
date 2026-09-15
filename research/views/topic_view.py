from rest_framework.viewsets import ModelViewSet
from research.models import Topic
from research.serializers import TopicSerializer


class TopicViewSet(ModelViewSet):

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
