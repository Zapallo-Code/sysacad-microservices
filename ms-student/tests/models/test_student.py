from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from app.models import DocumentType, Student


class StudentModelTest(TestCase):
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
        self.assertEqual(self.student.full_name, "Juan Pérez")

    def test_str_representation(self):
        expected = "Pérez, Juan - Student Number: 1001"
        self.assertEqual(str(self.student), expected)

    def test_repr_representation(self):
        expected = "<Student: Pérez, Juan>"
        self.assertEqual(repr(self.student), expected)

    def test_student_number_unique_constraint(self):
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
                specialty_id=2,
            )

    def test_gender_choices(self):
        genders = [("M", "Male"), ("F", "Female"), ("O", "Other")]
        for i, (gender_code, _gender_name) in enumerate(genders):
            student = Student.objects.create(
                first_name=f"Test{i}",
                last_name="Student",
                document_number=f"1111111{i}",
                birth_date=date(2000, 1, 1),
                gender=gender_code,
                student_number=2000 + i,
                enrollment_date=date(2023, 3, 1),
                document_type=self.document_type,
                specialty_id=1,
            )
            self.assertEqual(student.gender, gender_code)

    def test_document_type_relationship(self):
        self.assertEqual(self.student.document_type.name, "DNI")
        self.assertIn(self.student, self.document_type.students.all())

    def test_document_type_protect_on_delete(self):
        from django.db.models import ProtectedError

        with self.assertRaises(ProtectedError):
            self.document_type.delete()

    def test_created_at_auto_now_add(self):
        self.assertIsNotNone(self.student.created_at)

    def test_updated_at_auto_now(self):
        self.assertIsNotNone(self.student.updated_at)

    def test_meta_db_table(self):
        self.assertEqual(Student._meta.db_table, "students")

    def test_meta_verbose_name(self):
        self.assertEqual(Student._meta.verbose_name, "Student")
        self.assertEqual(Student._meta.verbose_name_plural, "Students")

    def test_meta_ordering(self):
        self.assertEqual(Student._meta.ordering, ["last_name", "first_name"])

    def test_ordering_multiple_students(self):
        Student.objects.create(
            first_name="Ana",
            last_name="Zapata",
            document_number="11111111",
            birth_date=date(2000, 1, 1),
            gender="F",
            student_number=1002,
            enrollment_date=date(2023, 3, 1),
            document_type=self.document_type,
            specialty_id=1,
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
            specialty_id=1,
        )

        students = list(Student.objects.all())
        self.assertEqual(students[0].last_name, "Garcia")
        self.assertEqual(students[1].last_name, "Pérez")
        self.assertEqual(students[2].last_name, "Zapata")

    def test_indexes_exist(self):
        index_fields = [idx.fields for idx in Student._meta.indexes]
        self.assertIn(["student_number"], index_fields)
        self.assertIn(["document_number"], index_fields)
        self.assertIn(["last_name", "first_name"], index_fields)

    def test_first_name_max_length(self):
        max_length = Student._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        max_length = Student._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    def test_document_number_max_length(self):
        max_length = Student._meta.get_field("document_number").max_length
        self.assertEqual(max_length, 50)

    def test_gender_max_length(self):
        max_length = Student._meta.get_field("gender").max_length
        self.assertEqual(max_length, 1)
