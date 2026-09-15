from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from research.models import Research
from research.serializers import ResearchSerializer


class ResearchViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer