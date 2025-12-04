from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, DocumentTypeViewSet, health_check


router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"document-types", DocumentTypeViewSet, basename="document-type")

urlpatterns = [
    path("health/", health_check, name="health-check"),
] + router.urls
