from datetime import date
from unittest.mock import Mock

import pytest

from app.models import DocumentType, Student
from app.services import StudentService


@pytest.fixture
def document_type(db):
    """Create a test document type."""
    return DocumentType.objects.create(
        name="DNI", description="Documento Nacional de Identidad"
    )


@pytest.fixture
def student_data(document_type):
    """Create sample student data."""
    return {
        "first_name": "Juan",
        "last_name": "Pérez",
        "document_number": "12345678",
        "birth_date": date(2000, 5, 15),
        "gender": "M",
        "student_number": 1001,
        "enrollment_date": date(2020, 3, 1),
        "document_type_id": document_type.id,
        "specialty_id": 1,
    }


@pytest.fixture
def existing_student(db, document_type):
    """Create an existing student for tests."""
    return Student.objects.create(
        first_name="Existing",
        last_name="Student",
        document_number="11111111",
        birth_date=date(2000, 1, 1),
        gender="M",
        student_number=9000,
        enrollment_date=date(2020, 1, 1),
        document_type=document_type,
        specialty_id=1,
    )


@pytest.fixture
def student_service():
    """Create a StudentService instance with mocked academic client."""
    mock_academic_client = Mock()
    mock_academic_client.validate_specialty.return_value = True
    return StudentService(academic_client=mock_academic_client)


@pytest.mark.django_db
class TestStudentService:
    def test_create_student(self, student_service, student_data):
        student = student_service.create(student_data)
        assert student.first_name == "Juan"
        assert student.last_name == "Pérez"
        assert student.id is not None

    def test_create_student_duplicate_student_number_raises_error(self, student_service, student_data, existing_student):
        data = student_data.copy()
        data["student_number"] = 9000
        with pytest.raises(ValueError, match="already taken"):
            student_service.create(data)

    def test_create_student_duplicate_document_number_raises_error(self, student_service, student_data, existing_student):
        data = student_data.copy()
        data["document_number"] = "11111111"
        with pytest.raises(ValueError, match="already registered"):
            student_service.create(data)

    def test_create_student_invalid_document_type_raises_error(self, student_service, student_data):
        data = student_data.copy()
        data["document_type_id"] = 9999
        with pytest.raises(ValueError, match="does not exist"):
            student_service.create(data)

    def test_find_by_id_existing(self, student_service, existing_student):
        found = student_service.find_by_id(existing_student.id)
        assert found is not None
        assert found.first_name == "Existing"

    def test_find_by_id_not_existing(self, student_service):
        found = student_service.find_by_id(9999)
        assert found is None

    def test_find_by_student_number_existing(self, student_service, existing_student):
        found = student_service.find_by_student_number(9000)
        assert found is not None
        assert found.id == existing_student.id

    def test_find_by_student_number_not_existing(self, student_service):
        found = student_service.find_by_student_number(8888)
        assert found is None

    def test_find_all(self, student_service, existing_student):
        students = student_service.find_all()
        assert len(students) >= 1

    def test_update_student(self, student_service, existing_student):
        updated = student_service.update(existing_student.id, {"first_name": "Updated"})
        assert updated.first_name == "Updated"

    def test_update_non_existing_raises_error(self, student_service):
        with pytest.raises(ValueError, match="does not exist"):
            student_service.update(9999, {"first_name": "Test"})

    def test_update_duplicate_student_number_raises_error(self, student_service, existing_student, document_type):
        Student.objects.create(
            first_name="Another",
            last_name="Student",
            document_number="22222222",
            birth_date=date(2000, 1, 1),
            gender="F",
            student_number=9001,
            enrollment_date=date(2020, 1, 1),
            document_type=document_type,
            specialty_id=1,
        )
        with pytest.raises(ValueError, match="already taken"):
            student_service.update(existing_student.id, {"student_number": 9001})

    def test_update_duplicate_document_number_raises_error(self, student_service, existing_student, document_type):
        Student.objects.create(
            first_name="Another",
            last_name="Student",
            document_number="33333333",
            birth_date=date(2000, 1, 1),
            gender="F",
            student_number=9002,
            enrollment_date=date(2020, 1, 1),
            document_type=document_type,
            specialty_id=1,
        )
        with pytest.raises(ValueError, match="already registered"):
            student_service.update(existing_student.id, {"document_number": "33333333"})

    def test_delete_by_id_existing(self, student_service, document_type):
        student = Student.objects.create(
            first_name="ToDelete",
            last_name="Student",
            document_number="44444444",
            birth_date=date(2000, 1, 1),
            gender="M",
            student_number=9003,
            enrollment_date=date(2020, 1, 1),
            document_type=document_type,
            specialty_id=1,
        )
        result = student_service.delete_by_id(student.id)
        assert result is True

    def test_delete_by_id_not_existing_raises_error(self, student_service):
        with pytest.raises(ValueError, match="does not exist"):
            student_service.delete_by_id(9999)

    def test_update_same_student_number_allowed(self, student_service, existing_student):
        updated = student_service.update(
            existing_student.id, {"student_number": 9000, "first_name": "Updated"}
        )
        assert updated.first_name == "Updated"
        assert updated.student_number == 9000

    def test_update_same_document_number_allowed(self, student_service, existing_student):
        updated = student_service.update(
            existing_student.id, {"document_number": "11111111", "first_name": "Updated"}
        )
        assert updated.first_name == "Updated"
        assert updated.document_number == "11111111"
