from datetime import date

from django.test import TestCase

from app.models import DocumentType, Student
from app.repositories import StudentRepository


class StudentRepositoryTest(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            name="DNI", description="Documento Nacional de Identidad"
        )
        self.student = Student.objects.create(
            first_name="Juan",
            last_name="Pérez",
            document_number="12345678",
            birth_date=date(2000, 5, 15),
            gender="M",
            student_number=1001,
            enrollment_date=date(2023, 3, 1),
            document_type=self.document_type,
            specialty_id=1,
        )

    def test_create_student(self):
        data = {
            "first_name": "María",
            "last_name": "García",
            "document_number": "87654321",
            "birth_date": date(2001, 8, 20),
            "gender": "F",
            "student_number": 1002,
            "enrollment_date": date(2023, 3, 1),
            "document_type": self.document_type,
            "specialty_id": 2,
        }
        student = StudentRepository.create(data)
        self.assertEqual(student.first_name, "María")
        self.assertEqual(student.last_name, "García")
        self.assertIsNotNone(student.id)

    def test_find_by_id_existing(self):
        found = StudentRepository.find_by_id(self.student.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.first_name, "Juan")

    def test_find_by_id_not_existing(self):
        found = StudentRepository.find_by_id(9999)
        self.assertIsNone(found)

    def test_find_by_student_number_existing(self):
        found = StudentRepository.find_by_student_number(1001)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, self.student.id)

    def test_find_by_student_number_not_existing(self):
        found = StudentRepository.find_by_student_number(9999)
        self.assertIsNone(found)

    def test_find_all(self):
        Student.objects.create(
            first_name="María",
            last_name="García",
            document_number="87654321",
            birth_date=date(2001, 8, 20),
            gender="F",
            student_number=1002,
            enrollment_date=date(2023, 3, 1),
            document_type=self.document_type,
            specialty_id=2,
        )
        all_students = StudentRepository.find_all()
        self.assertEqual(len(all_students), 2)

    def test_update_student(self):
        self.student.first_name = "Juan Carlos"
        updated = StudentRepository.update(self.student)
        self.assertEqual(updated.first_name, "Juan Carlos")

    def test_delete_by_id_existing(self):
        student = Student.objects.create(
            first_name="Test",
            last_name="Delete",
            document_number="11111111",
            birth_date=date(2000, 1, 1),
            gender="M",
            student_number=9999,
            enrollment_date=date(2023, 3, 1),
            document_type=self.document_type,
            specialty_id=1,
        )
        result = StudentRepository.delete_by_id(student.id)
        self.assertTrue(result)
        self.assertIsNone(StudentRepository.find_by_id(student.id))

    def test_delete_by_id_not_existing(self):
        result = StudentRepository.delete_by_id(9999)
        self.assertFalse(result)

    def test_exists_by_id_true(self):
        self.assertTrue(StudentRepository.exists_by_id(self.student.id))

    def test_exists_by_id_false(self):
        self.assertFalse(StudentRepository.exists_by_id(9999))

    def test_exists_by_student_number_true(self):
        self.assertTrue(StudentRepository.exists_by_student_number(1001))

    def test_exists_by_student_number_false(self):
        self.assertFalse(StudentRepository.exists_by_student_number(9999))

    def test_exists_by_document_number_true(self):
        self.assertTrue(StudentRepository.exists_by_document_number("12345678"))

    def test_exists_by_document_number_false(self):
        self.assertFalse(StudentRepository.exists_by_document_number("00000000"))

    def test_find_by_id_includes_document_type(self):
        found = StudentRepository.find_by_id(self.student.id)
        self.assertEqual(found.document_type.name, "DNI")
