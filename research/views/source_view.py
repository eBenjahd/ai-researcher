from rest_framework.viewsets import ModelViewSet
from research.serializers import SourceSerializer
from research.models import Source

class SourceViewSet(ModelViewSet):

    queryset = Source.objects.all()
    serializer_class = SourceSerializer