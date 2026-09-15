from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from research.models import Claim
from research.serializers import ClaimSerializer


class ClaimViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer