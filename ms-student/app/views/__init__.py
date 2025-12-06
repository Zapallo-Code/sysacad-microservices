from .base_viewset import BaseViewSet as BaseViewSet
from .document_type import DocumentTypeViewSet as DocumentTypeViewSet
from .health import health_check as health_check
from .student import StudentViewSet as StudentViewSet

__all__ = ["BaseViewSet", "StudentViewSet", "DocumentTypeViewSet", "health_check"]
