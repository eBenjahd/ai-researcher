from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    SourceViewSet, 
    DocumentViewSet, 
    TopicViewSet, 
    ClaimViewSet,
    ResearchViewSet,
    ResearchView,
)


router = DefaultRouter()
router.register("sources", SourceViewSet, basename="source")
router.register("documents", DocumentViewSet, basename="document")
router.register("topics", TopicViewSet, basename="topic")
router.register("claims", ClaimViewSet, basename="claim")
router.register("researchs", ResearchViewSet, basename="research")

urlpatterns = [path("research/run/", ResearchView.as_view(), name="research-run")]
urlpatterns += router.urls