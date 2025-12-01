from datetime import date
from django.test import TestCase
from django.db import IntegrityError
from app.models import Student, DocumentType


class StudentModelTest(TestCase):
    """Tests for the Student model."""

    def setUp(self):
        """Set up test data."""
        self.document_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
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
            specialty_id=1
        )

    def test_create_student(self):
        """Test creating a Student instance."""
        self.assertEqual(self.student.first_name, "Juan")
        self.assertEqual(self.student.last_name, "Pérez")
        self.assertEqual(self.student.document_number, "12345678")
        self.assertEqual(self.student.birth_date, date(2000, 5, 15))
        self.assertEqual(self.student.gender, "M")
        self.assertEqual(self.student.student_number, 1001)
        self.assertEqual(self.student.enrollment_date, date(2023, 3, 1))
        self.assertEqual(self.student.document_type, self.document_type)
        self.assertEqual(self.student.specialty_id, 1)

    def test_full_name_property(self):
        """Test the full_name property."""
        self.assertEqual(self.student.full_name, "Juan Pérez")

    def test_str_representation(self):
        """Test the string representation of Student."""
        expected = "Pérez, Juan - Student Number: 1001"
        self.assertEqual(str(self.student), expected)

    def test_repr_representation(self):
        """Test the repr representation of Student."""
        expected = "<Student: Pérez, Juan>"
        self.assertEqual(repr(self.student), expected)

    def test_student_number_unique_constraint(self):
        """Test that student_number must be unique."""
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                first_name="María",
                last_name="García",
                document_number="87654321",
                birth_date=date(2001, 8, 20),
                gender="F",
                student_number=1001,
                enrollment_date=date(2023, 3, 1),
                document_type=self.document_type,
                specialty_id=2
            )

    def test_gender_choices(self):
        """Test all valid gender choices."""
        genders = [("M", "Male"), ("F", "Female"), ("O", "Other")]
        for i, (gender_code, gender_name) in enumerate(genders):
            student = Student.objects.create(
                first_name=f"Test{i}",
                last_name="Student",
                document_number=f"1111111{i}",
                birth_date=date(2000, 1, 1),
                gender=gender_code,
                student_number=2000 + i,
                enrollment_date=date(2023, 3, 1),
                document_type=self.document_type,
                specialty_id=1
            )
            self.assertEqual(student.gender, gender_code)

    def test_document_type_relationship(self):
        """Test the relationship with DocumentType."""
        self.assertEqual(self.student.document_type.name, "DNI")
        self.assertIn(self.student, self.document_type.students.all())

    def test_document_type_protect_on_delete(self):
        """Test that deleting DocumentType with students raises ProtectedError."""
        from django.db.models import ProtectedError
        with self.assertRaises(ProtectedError):
            self.document_type.delete()

    def test_created_at_auto_now_add(self):
        """Test that created_at is automatically set."""
        self.assertIsNotNone(self.student.created_at)

    def test_updated_at_auto_now(self):
        """Test that updated_at is automatically set."""
        self.assertIsNotNone(self.student.updated_at)

    def test_meta_db_table(self):
        """Test the database table name."""
        self.assertEqual(Student._meta.db_table, "students")

    def test_meta_verbose_name(self):
        """Test the verbose name."""
        self.assertEqual(Student._meta.verbose_name, "Student")
        self.assertEqual(Student._meta.verbose_name_plural, "Students")

    def test_meta_ordering(self):
        """Test the default ordering."""
        self.assertEqual(Student._meta.ordering, ["last_name", "first_name"])

    def test_ordering_multiple_students(self):
        """Test that students are ordered by last_name, then first_name."""
        Student.objects.create(
            first_name="Ana",
            last_name="Zapata",
            document_number="11111111",
            birth_date=date(2000, 1, 1),
            gender="F",
            student_number=1002,
            enrollment_date=date(2023, 3, 1),
            document_type=self.document_type,
            specialty_id=1
        )
        Student.objects.create(
            first_name="Carlos",
            last_name="Garcia",
            document_number="22222222",
            birth_date=date(2000, 1, 1),
            gender="M",
            student_number=1003,
            enrollment_date=date(2023, 3, 1),
            document_type=self.document_type,
            specialty_id=1
        )
        
        students = list(Student.objects.all())
        self.assertEqual(students[0].last_name, "Garcia")
        self.assertEqual(students[1].last_name, "Pérez")
        self.assertEqual(students[2].last_name, "Zapata")

    def test_indexes_exist(self):
        """Test that the expected indexes are defined."""
        index_fields = [idx.fields for idx in Student._meta.indexes]
        self.assertIn(["student_number"], index_fields)
        self.assertIn(["document_number"], index_fields)
        self.assertIn(["last_name", "first_name"], index_fields)

    def test_first_name_max_length(self):
        """Test first_name max_length constraint."""
        max_length = Student._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        """Test last_name max_length constraint."""
        max_length = Student._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    def test_document_number_max_length(self):
        """Test document_number max_length constraint."""
        max_length = Student._meta.get_field("document_number").max_length
        self.assertEqual(max_length, 50)

    def test_gender_max_length(self):
        """Test gender max_length constraint."""
        max_length = Student._meta.get_field("gender").max_length
        self.assertEqual(max_length, 1)
