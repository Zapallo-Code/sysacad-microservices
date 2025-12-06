from typing import Any

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import QuerySet
from django.utils import timezone

from app.models import Student


class StudentRepository:
    @staticmethod
    def _get_active_queryset() -> QuerySet[Student]:
        return Student.objects.filter(is_active=True, deleted_at__isnull=True)

    @staticmethod
    def create(student_data: dict[str, Any]) -> Student:
        student = Student(**student_data)
        student.full_clean()
        student.save()
        return student

    @staticmethod
    def find_by_id(id: int) -> Student | None:
        try:
            return StudentRepository._get_active_queryset().select_related("document_type").get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_student_number(student_number: int) -> Student | None:
        try:
            return StudentRepository._get_active_queryset().select_related("document_type").get(
                student_number=student_number
            )
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def find_all() -> QuerySet[Student]:
        return StudentRepository._get_active_queryset().select_related("document_type")

    @staticmethod
    def find_by_specialty(specialty_id: int) -> QuerySet[Student]:
        return StudentRepository._get_active_queryset().filter(
            specialty_id=specialty_id
        ).select_related("document_type")

    @staticmethod
    def update(student: Student) -> Student:
        student.full_clean()
        student.save()
        return student

    @staticmethod
    def delete_by_id(id: int) -> bool:
        try:
            student = Student.objects.get(id=id)
            student.is_active = False
            student.deleted_at = timezone.now()
            student.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return StudentRepository._get_active_queryset().filter(id=id).exists()

    @staticmethod
    def exists_by_student_number(student_number: int) -> bool:
        return StudentRepository._get_active_queryset().filter(student_number=student_number).exists()

    @staticmethod
    def exists_by_document_number(document_number: str) -> bool:
        return StudentRepository._get_active_queryset().filter(document_number=document_number).exists()
