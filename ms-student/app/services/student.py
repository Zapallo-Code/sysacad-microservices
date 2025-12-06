import logging

from django.core.cache import cache
from django.db import transaction

from app.models import Student
from app.repositories import DocumentTypeRepository, StudentRepository
from app.utils.academic_client import AcademicServiceClient, academic_service_client

logger = logging.getLogger(__name__)


class StudentService:
    def __init__(
        self,
        student_repository: StudentRepository = None,
        document_type_repository: DocumentTypeRepository = None,
        academic_client: AcademicServiceClient = None
    ):
        """Inicializa el servicio con sus dependencias.
        
        Args:
            student_repository: Repository para estudiantes (default: StudentRepository)
            document_type_repository: Repository para tipos de documento (default: DocumentTypeRepository)
            academic_client: Cliente del servicio académico (default: academic_service_client singleton)
        """
        self.student_repository = student_repository or StudentRepository
        self.document_type_repository = document_type_repository or DocumentTypeRepository
        self.academic_client = academic_client or academic_service_client

    def _validate_unique_student_number(self, student_number: int, exclude_id: int = None):
        """Valida que el student_number sea único."""
        existing = self.student_repository.find_by_student_number(student_number)
        if existing and (exclude_id is None or existing.id != exclude_id):
            logger.error(f"Student number {student_number} already exists")
            raise ValueError(f"Student number {student_number} is already taken")

    def _validate_unique_document_number(self, document_number: str, exclude_id: int = None):
        """Valida que el document_number sea único."""
        if self.student_repository.exists_by_document_number(document_number):
            logger.error(f"Document number {document_number} already registered")
            raise ValueError(f"Document number {document_number} is already registered")

    def _validate_specialty_exists(self, specialty_id: int):
        """Valida que la especialidad exista en el microservicio académico."""
        if not self.academic_client.validate_specialty(specialty_id):
            logger.error(f"Specialty {specialty_id} not found in academic service")
            raise ValueError(f"Specialty with id {specialty_id} does not exist")

    def _validate_document_type_exists(self, document_type_id: int):
        """Valida que el tipo de documento exista."""
        if not self.document_type_repository.exists_by_id(document_type_id):
            logger.error(f"Document type with id {document_type_id} not found")
            raise ValueError(f"Document type with id {document_type_id} does not exist")

    def _update_entity_fields(self, entity, data: dict):
        """Actualiza campos de una entidad con los datos proporcionados."""
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        return entity

    @transaction.atomic
    def create(self, student_data: dict) -> Student:
        self._validate_unique_student_number(student_data.get("student_number"))
        self._validate_unique_document_number(student_data.get("document_number"))
        
        specialty_id = student_data.get("specialty_id")
        if specialty_id:
            self._validate_specialty_exists(specialty_id)
        
        self._validate_document_type_exists(student_data.get("document_type_id"))
        student = self.student_repository.create(student_data)
        # Invalidate cache
        cache.delete("students:all")
        return student

    def find_by_id(self, id: int) -> Student | None:
        """Obtiene estudiante por ID con caché."""
        cache_key = f"student:{id}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"Cache hit for student:{id}")
            return cached
        
        student = self.student_repository.find_by_id(id)
        if student:
            cache.set(cache_key, student, timeout=300)  # 5 minutes
        return student

    def find_by_student_number(self, student_number: int) -> Student | None:
        return self.student_repository.find_by_student_number(student_number)

    def find_all(self) -> list[Student]:
        """Obtiene todos los estudiantes con caché."""
        cache_key = "students:all"
        cached = cache.get(cache_key)
        if cached:
            logger.debug("Cache hit for students:all")
            return cached
        
        students = list(self.student_repository.find_all())
        cache.set(cache_key, students, timeout=600)  # 10 minutes
        return students

    def find_by_specialty(self, specialty_id: int):
        self._validate_specialty_exists(specialty_id)
        return self.student_repository.find_by_specialty(specialty_id)

    @transaction.atomic
    def update(self, id: int, student_data: dict) -> Student:
        existing_student = self.student_repository.find_by_id(id)
        if not existing_student:
            logger.error(f"Student with id {id} not found for update")
            raise ValueError(f"Student with id {id} does not exist")

        student_number = student_data.get("student_number")
        if student_number and student_number != existing_student.student_number:
            self._validate_unique_student_number(student_number, exclude_id=id)

        document_number = student_data.get("document_number")
        if document_number and document_number != existing_student.document_number:
            self._validate_unique_document_number(document_number, exclude_id=id)

        document_type_id = student_data.get("document_type_id")
        if document_type_id is not None and document_type_id != existing_student.document_type_id:
            self._validate_document_type_exists(document_type_id)

        specialty_id = student_data.get("specialty_id")
        if specialty_id and specialty_id != existing_student.specialty_id:
            self._validate_specialty_exists(specialty_id)

        self._update_entity_fields(existing_student, student_data)
        updated = self.student_repository.update(existing_student)
        # Invalidate cache
        cache.delete(f"student:{id}")
        cache.delete("students:all")
        return updated

    @transaction.atomic
    def delete_by_id(self, id: int) -> bool:
        if not self.student_repository.exists_by_id(id):
            logger.error(f"Student with id {id} not found for deletion")
            raise ValueError(f"Student with id {id} does not exist")
        result = self.student_repository.delete_by_id(id)
        # Invalidate cache
        cache.delete(f"student:{id}")
        cache.delete("students:all")
        return result


