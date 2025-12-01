from datetime import date
from django.test import TestCase
from app.models import Student, DocumentType
from app.services import StudentService


class StudentServiceTest(TestCase):
    """Tests for StudentService."""

    def setUp(self):
        """Set up test data."""
        self.document_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
        )
        self.student_data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "document_number": "12345678",
            "birth_date": date(2000, 5, 15),
            "gender": "M",
            "student_number": 1001,
            "enrollment_date": date(2020, 3, 1),
            "document_type_id": self.document_type.id,
            "specialty_id": 1
        }
        self.student = Student.objects.create(
            first_name="Existing",
            last_name="Student",
            document_number="11111111",
            birth_date=date(2000, 1, 1),
            gender="M",
            student_number=9000,
            enrollment_date=date(2020, 1, 1),
            document_type=self.document_type,
            specialty_id=1
        )

    def test_create_student(self):
        """Test creating a student through service."""
        student = StudentService.create(self.student_data)
        self.assertEqual(student.first_name, "Juan")
        self.assertEqual(student.last_name, "Pérez")
        self.assertIsNotNone(student.id)

    def test_create_student_duplicate_student_number_raises_error(self):
        """Test creating a student with duplicate student number raises ValueError."""
        data = self.student_data.copy()
        data["student_number"] = 9000
        with self.assertRaises(ValueError) as context:
            StudentService.create(data)
        self.assertIn("already taken", str(context.exception))

    def test_create_student_duplicate_document_number_raises_error(self):
        """Test creating a student with duplicate document number raises ValueError."""
        data = self.student_data.copy()
        data["document_number"] = "11111111"
        with self.assertRaises(ValueError) as context:
            StudentService.create(data)
        self.assertIn("already registered", str(context.exception))

    def test_create_student_invalid_document_type_raises_error(self):
        """Test creating a student with invalid document type raises ValueError."""
        data = self.student_data.copy()
        data["document_type_id"] = 9999
        with self.assertRaises(ValueError) as context:
            StudentService.create(data)
        self.assertIn("does not exist", str(context.exception))

    def test_find_by_id_existing(self):
        """Test finding an existing student by id."""
        found = StudentService.find_by_id(self.student.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.first_name, "Existing")

    def test_find_by_id_not_existing(self):
        """Test finding a non-existing student by id."""
        found = StudentService.find_by_id(9999)
        self.assertIsNone(found)

    def test_find_by_student_number_existing(self):
        """Test finding a student by student number."""
        found = StudentService.find_by_student_number(9000)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, self.student.id)

    def test_find_by_student_number_not_existing(self):
        """Test finding a non-existing student by student number."""
        found = StudentService.find_by_student_number(8888)
        self.assertIsNone(found)

    def test_find_all(self):
        """Test finding all students."""
        students = StudentService.find_all()
        self.assertGreaterEqual(len(students), 1)

    def test_update_student(self):
        """Test updating a student."""
        updated = StudentService.update(
            self.student.id,
            {"first_name": "Updated"}
        )
        self.assertEqual(updated.first_name, "Updated")

    def test_update_non_existing_raises_error(self):
        """Test updating a non-existing student raises ValueError."""
        with self.assertRaises(ValueError) as context:
            StudentService.update(9999, {"first_name": "Test"})
        self.assertIn("does not exist", str(context.exception))

    def test_update_duplicate_student_number_raises_error(self):
        """Test updating with duplicate student number raises ValueError."""
        Student.objects.create(
            first_name="Another",
            last_name="Student",
            document_number="22222222",
            birth_date=date(2000, 1, 1),
            gender="F",
            student_number=9001,
            enrollment_date=date(2020, 1, 1),
            document_type=self.document_type,
            specialty_id=1
        )
        with self.assertRaises(ValueError) as context:
            StudentService.update(self.student.id, {"student_number": 9001})
        self.assertIn("already taken", str(context.exception))

    def test_update_duplicate_document_number_raises_error(self):
        """Test updating with duplicate document number raises ValueError."""
        Student.objects.create(
            first_name="Another",
            last_name="Student",
            document_number="33333333",
            birth_date=date(2000, 1, 1),
            gender="F",
            student_number=9002,
            enrollment_date=date(2020, 1, 1),
            document_type=self.document_type,
            specialty_id=1
        )
        with self.assertRaises(ValueError) as context:
            StudentService.update(self.student.id, {"document_number": "33333333"})
        self.assertIn("already registered", str(context.exception))

    def test_delete_by_id_existing(self):
        """Test deleting an existing student."""
        student = Student.objects.create(
            first_name="ToDelete",
            last_name="Student",
            document_number="44444444",
            birth_date=date(2000, 1, 1),
            gender="M",
            student_number=9003,
            enrollment_date=date(2020, 1, 1),
            document_type=self.document_type,
            specialty_id=1
        )
        result = StudentService.delete_by_id(student.id)
        self.assertTrue(result)

    def test_delete_by_id_not_existing_raises_error(self):
        """Test deleting a non-existing student raises ValueError."""
        with self.assertRaises(ValueError) as context:
            StudentService.delete_by_id(9999)
        self.assertIn("does not exist", str(context.exception))

    def test_calculate_age(self):
        """Test calculating student age."""
        age = StudentService.calculate_age(self.student)
        expected_age = date.today().year - 2000
        if (date.today().month, date.today().day) < (1, 1):
            expected_age -= 1
        self.assertEqual(age, expected_age)

    def test_calculate_age_none_student(self):
        """Test calculate_age returns None for None student."""
        age = StudentService.calculate_age(None)
        self.assertIsNone(age)

    def test_is_enrollment_valid_true(self):
        """Test is_enrollment_valid returns True for valid enrollment."""
        birth_date = date(2000, 1, 1)
        enrollment_date = date(2020, 1, 1)
        result = StudentService.is_enrollment_valid(birth_date, enrollment_date)
        self.assertTrue(result)

    def test_is_enrollment_valid_false_too_young(self):
        """Test is_enrollment_valid returns False if too young."""
        birth_date = date(2010, 1, 1)
        enrollment_date = date(2020, 1, 1)
        result = StudentService.is_enrollment_valid(birth_date, enrollment_date)
        self.assertFalse(result)

    def test_is_enrollment_valid_false_before_birth(self):
        """Test is_enrollment_valid returns False if enrollment before birth."""
        birth_date = date(2000, 1, 1)
        enrollment_date = date(1999, 1, 1)
        result = StudentService.is_enrollment_valid(birth_date, enrollment_date)
        self.assertFalse(result)

    def test_update_same_student_number_allowed(self):
        """Test updating with same student number is allowed."""
        updated = StudentService.update(
            self.student.id,
            {"student_number": 9000, "first_name": "Updated"}
        )
        self.assertEqual(updated.first_name, "Updated")
        self.assertEqual(updated.student_number, 9000)

    def test_update_same_document_number_allowed(self):
        """Test updating with same document number is allowed."""
        updated = StudentService.update(
            self.student.id,
            {"document_number": "11111111", "first_name": "Updated"}
        )
        self.assertEqual(updated.first_name, "Updated")
        self.assertEqual(updated.document_number, "11111111")
