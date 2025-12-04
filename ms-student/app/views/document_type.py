from app.serializers import DocumentTypeSerializer
from app.services import DocumentTypeService
from app.views.base_viewset import BaseViewSet


class DocumentTypeViewSet(BaseViewSet):
    serializer_class = DocumentTypeSerializer
    service_class = DocumentTypeService
    entity_name = "Document type"
