import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import StudentSerializer
from app.services import StudentService

logger = logging.getLogger(__name__)


class StudentViewSet(viewsets.ViewSet):
    serializer_class = StudentSerializer

    def list(self, request):
            students = StudentService.find_all()
            serializer = self.serializer_class(students, many=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
            student = StudentService.find_by_id(int(pk))
            if student is None:
                return Response(
                    {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(student)
            return Response(serializer.data)

    def create(self, request):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            student = StudentService.create(serializer.validated_data)
            response_serializer = self.serializer_class(student)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk=None):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_student = StudentService.update(int(pk), serializer.validated_data)
            response_serializer = self.serializer_class(updated_student)
            return Response(response_serializer.data)


    def destroy(self, request, pk=None):
            StudentService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)