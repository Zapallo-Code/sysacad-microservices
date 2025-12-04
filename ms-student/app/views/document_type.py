from rest_framework import status, viewsets
from rest_framework.response import Response

from app.serializers import DocumentTypeSerializer
from app.services import DocumentTypeService


class DocumentTypeViewSet(viewsets.ViewSet):
    serializer_class = DocumentTypeSerializer

    def list(self, request):
        document_types = DocumentTypeService.find_all()
        serializer = self.serializer_class(document_types, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        document_type = DocumentTypeService.find_by_id(int(pk))
        if document_type is None:
            return Response(
                {"error": "Document type not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(document_type)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_type = DocumentTypeService.create(serializer.validated_data)
        response_serializer = self.serializer_class(document_type)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_document_type = DocumentTypeService.update(int(pk), serializer.validated_data)
        response_serializer = self.serializer_class(updated_document_type)
        return Response(response_serializer.data)

    def partial_update(self, request, pk=None):
        document_type = DocumentTypeService.find_by_id(int(pk))
        if document_type is None:
            return Response(
                {"error": "Document type not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(document_type, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_document_type = DocumentTypeService.update(int(pk), serializer.validated_data)
        response_serializer = self.serializer_class(updated_document_type)
        return Response(response_serializer.data)

    def destroy(self, request, pk=None):
        DocumentTypeService.delete_by_id(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
