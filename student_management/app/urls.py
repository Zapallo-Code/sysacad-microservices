from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, DocumentTypeViewSet


router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"document-types", DocumentTypeViewSet, basename="document-type")

urlpatterns = router.urls
