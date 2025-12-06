from app.serializers import StudentSerializer
from app.services import StudentService
from app.views.base_viewset import BaseViewSet


class StudentViewSet(BaseViewSet):
    serializer_class = StudentSerializer
    service_class = StudentService
    entity_name = "Student"
    paginate = True
