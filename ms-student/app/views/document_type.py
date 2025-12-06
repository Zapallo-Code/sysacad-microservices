from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from app.serializers import DocumentTypeSerializer
from app.services import DocumentTypeService


class DocumentTypeViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    serializer_class = DocumentTypeSerializer
    service_class = DocumentTypeService

    def get_queryset(self):
        return self.service_class().find_all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.service_class().find_by_id(int(kwargs["pk"]))
            if instance is None:
                return Response(
                    {"error": "Document type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
