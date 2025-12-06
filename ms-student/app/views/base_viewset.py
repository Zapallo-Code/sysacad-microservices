from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BaseViewSet(viewsets.ViewSet):
    serializer_class = None
    service_class = None
    entity_name = "Entity"
    paginate = False

    def get_service(self):
        if not hasattr(self, '_service_instance'):
            self._service_instance = self.service_class()
        return self._service_instance

    def list(self, request):
        entities = self.get_service().find_all()
        if self.paginate:
            paginator = PageNumberPagination()
            paginated_entities = paginator.paginate_queryset(entities, request)
            serializer = self.serializer_class(paginated_entities, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(entities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        entity = self.get_service().find_by_id(int(pk))
        if entity is None:
            return Response(
                {"error": f"{self.entity_name} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(entity)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        entity = self.get_service().create(serializer.validated_data)
        return Response(
            self.serializer_class(entity).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        entity = self.get_service().find_by_id(int(pk))
        if entity is None:
            return Response(
                {"error": f"{self.entity_name} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(entity, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_entity = self.get_service().update(int(pk), serializer.validated_data)
        return Response(self.serializer_class(updated_entity).data)

    def partial_update(self, request, pk=None):
        entity = self.get_service().find_by_id(int(pk))
        if entity is None:
            return Response(
                {"error": f"{self.entity_name} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(entity, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_entity = self.get_service().update(int(pk), serializer.validated_data)
        return Response(self.serializer_class(updated_entity).data)

    def destroy(self, request, pk=None):
        result = self.get_service().delete_by_id(int(pk))
        if not result:
            return Response(
                {"error": f"{self.entity_name} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
