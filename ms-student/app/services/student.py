import logging

from django.db import transaction

from app.models import Student
from app.repositories import DocumentTypeRepository, StudentRepository

logger = logging.getLogger(__name__)


class StudentService:
    @staticmethod
    @transaction.atomic
    def create(student_data: dict) -> Student:
        logger.info(
            f"Creating student: {student_data.get('first_name')} {student_data.get('last_name')}"
        )

        if StudentRepository.exists_by_student_number(student_data.get("student_number")):
            logger.error(f"Student number {student_data.get('student_number')} already exists")
            raise ValueError(
                f"Student number {student_data.get('student_number')} is already taken"
            )

        if StudentRepository.exists_by_document_number(student_data.get("document_number")):
            logger.error(
                f"Document number {student_data.get('document_number')} already registered"
            )
            raise ValueError(
                f"Document number {student_data.get('document_number')} is already registered"
            )

        # TODO: Validate specialty_id when Specialty microservice is available

        if not DocumentTypeRepository.exists_by_id(student_data.get("document_type_id")):
            logger.error(f"Document type with id {student_data.get('document_type_id')} not found")
            raise ValueError(
                f"Document type with id {student_data.get('document_type_id')} does not exist"
            )

        created_student = StudentRepository.create(student_data)
        logger.info(f"Student created successfully with id: {created_student.id}")
        return created_student

    @staticmethod
    def find_by_id(id: int) -> Student | None:
        logger.info(f"Finding student with id: {id}")
        student = StudentRepository.find_by_id(id)
        if not student:
            logger.warning(f"Student with id {id} not found")
        return student

    @staticmethod
    def find_by_student_number(student_number: int) -> Student | None:
        logger.info(f"Finding student with student number: {student_number}")
        student = StudentRepository.find_by_student_number(student_number)
        if not student:
            logger.warning(f"Student with student number {student_number} not found")
        return student

    @staticmethod
    def find_all() -> list[Student]:
        logger.info("Finding all students")
        students = StudentRepository.find_all()
        logger.info(f"Found {len(students)} students")
        return students

    @staticmethod
    def find_by_specialty(specialty_id: int) -> list[Student]:
        logger.info(f"Finding students by specialty id: {specialty_id}")

        # TODO: Validate specialty_id when Specialty microservice is available

        students = StudentRepository.find_by_specialty(specialty_id)
        logger.info(f"Found {len(students)} students in specialty {specialty_id}")
        return students

    @staticmethod
    @transaction.atomic
    def update(id: int, student_data: dict) -> Student:
        logger.info(f"Updating student with id: {id}")

        existing_student = StudentRepository.find_by_id(id)
        if not existing_student:
            logger.error(f"Student with id {id} not found for update")
            raise ValueError(f"Student with id {id} does not exist")

        student_number = student_data.get("student_number")
        if student_number and student_number != existing_student.student_number:
            if StudentRepository.exists_by_student_number(student_number):
                logger.error(f"Student number {student_number} already exists")
                raise ValueError(f"Student number {student_number} is already taken")

        document_number = student_data.get("document_number")
        if document_number and document_number != existing_student.document_number:
            if StudentRepository.exists_by_document_number(document_number):
                logger.error(f"Document number {document_number} already registered")
                raise ValueError(f"Document number {document_number} is already registered")

        document_type_id = student_data.get("document_type_id")
        if document_type_id is not None and document_type_id != existing_student.document_type_id:
            if not DocumentTypeRepository.exists_by_id(document_type_id):
                logger.error(f"Document type with id {document_type_id} not found")
                raise ValueError(f"Document type with id {document_type_id} does not exist")

        # TODO: Validate specialty_id when Specialty microservice is available

        for key, value in student_data.items():
            if hasattr(existing_student, key):
                setattr(existing_student, key, value)

        updated_student = StudentRepository.update(existing_student)
        logger.info(f"Student with id {id} updated successfully")
        return updated_student

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting student with id: {id}")

        if not StudentRepository.exists_by_id(id):
            logger.error(f"Student with id {id} not found for deletion")
            raise ValueError(f"Student with id {id} does not exist")

        result = StudentRepository.delete_by_id(id)
        logger.info(f"Student with id {id} deleted successfully")
        return result


