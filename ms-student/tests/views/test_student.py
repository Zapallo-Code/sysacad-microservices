from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.models import DocumentType, Student


class StudentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
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
            enrollment_date=date(2020, 3, 1),
            document_type=self.document_type,
            specialty_id=1,
        )
        self.list_url = "/api/v1/students/"
        self.detail_url = f"/api/v1/students/{self.student.id}/"
        self.valid_data = {
            "first_name": "María",
            "last_name": "García",
            "document_number": "87654321",
            "document_type_id": self.document_type.id,
            "birth_date": "2001-08-20",
            "gender": "F",
            "student_number": 1002,
            "enrollment_date": "2020-03-01",
            "specialty_id": 2,
        }

    def test_list_students(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_student(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Juan")
        self.assertEqual(response.data["last_name"], "Pérez")

    def test_retrieve_student_not_found(self):
        response = self.client.get("/students/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_student(self):
        response = self.client.post(self.list_url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "María")
        self.assertEqual(response.data["last_name"], "García")

    def test_create_student_invalid_first_name(self):
        data = self.valid_data.copy()
        data["first_name"] = "J"
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)

    def test_create_student_invalid_gender(self):
        data = self.valid_data.copy()
        data["gender"] = "X"
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("gender", response.data)

    def test_create_student_missing_required_fields(self):
        data = {"first_name": "Test"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_duplicate_student_number(self):
        data = self.valid_data.copy()
        data["student_number"] = 1001
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_duplicate_document_number(self):
        data = self.valid_data.copy()
        data["document_number"] = "12345678"
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_invalid_document_type(self):
        data = self.valid_data.copy()
        data["document_type_id"] = 9999
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student(self):
        data = {
            "first_name": "Juan Carlos",
            "last_name": "Pérez",
            "document_number": "12345678",
            "document_type_id": self.document_type.id,
            "birth_date": "2000-05-15",
            "gender": "M",
            "student_number": 1001,
            "enrollment_date": "2020-03-01",
            "specialty_id": 1,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Juan Carlos")

    def test_update_student_invalid_data(self):
        data = {
            "first_name": "J",
            "last_name": "Pérez",
            "document_number": "12345678",
            "document_type_id": self.document_type.id,
            "birth_date": "2000-05-15",
            "gender": "M",
            "student_number": 1001,
            "enrollment_date": "2020-03-01",
            "specialty_id": 1,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_student(self):
        student = Student.objects.create(
            first_name="ToDelete",
            last_name="Student",
            document_number="99999999",
            birth_date=date(2000, 1, 1),
            gender="M",
            student_number=9999,
            enrollment_date=date(2020, 1, 1),
            document_type=self.document_type,
            specialty_id=1,
        )
        response = self.client.delete(f"/api/v1/students/{student.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_student_birth_date_future(self):
        data = self.valid_data.copy()
        data["birth_date"] = "2030-01-01"
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data)

    def test_create_student_enrollment_before_birth(self):
        data = self.valid_data.copy()
        data["birth_date"] = "2000-01-01"
        data["enrollment_date"] = "1999-01-01"
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_contains_all_fields(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = [
            "id",
            "first_name",
            "last_name",
            "document_number",
            "document_type_id",
            "birth_date",
            "gender",
            "student_number",
            "enrollment_date",
            "specialty_id",
            "created_at",
            "updated_at",
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_students_url_exists(self):
        response = self.client.get("/api/v1/students/")
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_students_detail_url_format(self):
        response = self.client.get(f"/api/v1/students/{self.student.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
