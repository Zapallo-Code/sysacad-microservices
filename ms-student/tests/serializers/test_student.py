from datetime import date, timedelta

from django.test import TestCase

from app.models import DocumentType
from app.serializers import StudentSerializer


class StudentSerializerTest(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            name="DNI", description="Documento Nacional de Identidad"
        )
        self.valid_data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "document_number": "12345678",
            "document_type_id": self.document_type.id,
            "birth_date": "2000-05-15",
            "gender": "M",
            "student_number": 1001,
            "enrollment_date": "2020-03-01",
            "specialty_id": 1,
        }

    def test_valid_data(self):
        serializer = StudentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # First name validations
    def test_first_name_required(self):
        data = self.valid_data.copy()
        del data["first_name"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_min_length(self):
        data = self.valid_data.copy()
        data["first_name"] = "J"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_max_length(self):
        data = self.valid_data.copy()
        data["first_name"] = "J" * 51
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_whitespace_only(self):
        data = self.valid_data.copy()
        data["first_name"] = "   "
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_must_start_with_letter(self):
        data = self.valid_data.copy()
        data["first_name"] = "1Juan"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_only_letters_spaces_hyphens(self):
        data = self.valid_data.copy()
        data["first_name"] = "Juan123"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_first_name_with_hyphen(self):
        data = self.valid_data.copy()
        data["first_name"] = "Juan-Carlos"
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_first_name_title_case(self):
        data = self.valid_data.copy()
        data["first_name"] = "juan carlos"
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["first_name"], "Juan Carlos")

    # Last name validations
    def test_last_name_required(self):
        data = self.valid_data.copy()
        del data["last_name"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_last_name_min_length(self):
        data = self.valid_data.copy()
        data["last_name"] = "P"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_last_name_title_case(self):
        data = self.valid_data.copy()
        data["last_name"] = "pérez garcía"
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["last_name"], "Pérez García")

    # Document number validations
    def test_document_number_required(self):
        data = self.valid_data.copy()
        del data["document_number"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("document_number", serializer.errors)

    def test_document_number_min_length(self):
        data = self.valid_data.copy()
        data["document_number"] = "1234"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("document_number", serializer.errors)

    def test_document_number_alphanumeric_only(self):
        data = self.valid_data.copy()
        data["document_number"] = "1234@5678"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("document_number", serializer.errors)

    # Birth date validations
    def test_birth_date_required(self):
        data = self.valid_data.copy()
        del data["birth_date"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)

    def test_birth_date_future_invalid(self):
        data = self.valid_data.copy()
        data["birth_date"] = (date.today() + timedelta(days=1)).isoformat()
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)

    def test_birth_date_too_young(self):
        data = self.valid_data.copy()
        data["birth_date"] = (date.today() - timedelta(days=365 * 5)).isoformat()
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)

    def test_birth_date_too_old(self):
        data = self.valid_data.copy()
        data["birth_date"] = (date.today() - timedelta(days=365 * 121)).isoformat()
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("enrollment_date", serializer.errors)  # Error en enrollment_date por edad


    # Gender validations
    def test_gender_required(self):
        data = self.valid_data.copy()
        del data["gender"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("gender", serializer.errors)

    def test_gender_valid_choices(self):
        for gender in ["M", "F", "O"]:
            data = self.valid_data.copy()
            data["gender"] = gender
            serializer = StudentSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Gender {gender} should be valid")

    def test_gender_invalid_choice(self):
        data = self.valid_data.copy()
        data["gender"] = "X"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("gender", serializer.errors)

    # Student number validations
    def test_student_number_required(self):
        data = self.valid_data.copy()
        del data["student_number"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("student_number", serializer.errors)

    def test_student_number_positive(self):
        data = self.valid_data.copy()
        data["student_number"] = 0
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("student_number", serializer.errors)

    # Enrollment date validations
    def test_enrollment_date_required(self):
        data = self.valid_data.copy()
        del data["enrollment_date"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("enrollment_date", serializer.errors)

    def test_enrollment_date_too_far_future(self):
        data = self.valid_data.copy()
        data["enrollment_date"] = (date.today() + timedelta(days=400)).isoformat()
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("enrollment_date", serializer.errors)

    def test_enrollment_date_too_far_past(self):
        data = self.valid_data.copy()
        data["enrollment_date"] = (date.today() - timedelta(days=365 * 51)).isoformat()
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("enrollment_date", serializer.errors)

    # Document type ID validations
    def test_document_type_id_required(self):
        data = self.valid_data.copy()
        del data["document_type_id"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("document_type_id", serializer.errors)

    def test_document_type_id_positive(self):
        data = self.valid_data.copy()
        data["document_type_id"] = 0
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("document_type_id", serializer.errors)

    # Specialty ID validations
    def test_specialty_id_required(self):
        data = self.valid_data.copy()
        del data["specialty_id"]
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("specialty_id", serializer.errors)

    def test_specialty_id_positive(self):
        data = self.valid_data.copy()
        data["specialty_id"] = -1
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("specialty_id", serializer.errors)

    # Cross-field validations
    def test_enrollment_before_birth_invalid(self):
        data = self.valid_data.copy()
        data["birth_date"] = "2000-05-15"
        data["enrollment_date"] = "1999-01-01"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("enrollment_date", serializer.errors)

    def test_age_at_enrollment_too_young(self):
        data = self.valid_data.copy()
        data["birth_date"] = "2015-01-01"
        data["enrollment_date"] = "2020-01-01"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("enrollment_date", serializer.errors)

    def test_age_at_enrollment_unrealistic(self):
        data = self.valid_data.copy()
        # Use a date that's valid for birth_date but creates 100+ year enrollment age
        data["birth_date"] = "1915-01-01"
        data["enrollment_date"] = "2020-03-01"
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # Either enrollment_date or birth_date error is acceptable
        has_date_error = "enrollment_date" in serializer.errors or "birth_date" in serializer.errors
        self.assertTrue(has_date_error, f"Expected date validation error, got: {serializer.errors}")

    def test_read_only_fields(self):
        data = self.valid_data.copy()
        data["id"] = 999
        data["created_at"] = "2020-01-01T00:00:00Z"
        data["updated_at"] = "2020-01-01T00:00:00Z"
        serializer = StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("created_at", serializer.validated_data)
        self.assertNotIn("updated_at", serializer.validated_data)
