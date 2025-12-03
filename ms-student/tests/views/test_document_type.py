from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from app.models import DocumentType


class DocumentTypeViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.document_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
        )
        self.list_url = "/document-types/"
        self.detail_url = f"/document-types/{self.document_type.id}/"

    def test_list_document_types(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_document_type(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "DNI")

    def test_retrieve_document_type_not_found(self):
        response = self.client.get("/document-types/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_document_type(self):
        data = {"name": "LC", "description": "Libreta Cívica"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "LC")

    def test_create_document_type_invalid_data(self):
        data = {"name": "INVALID"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_document_type_missing_name(self):
        data = {"description": "Test"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_document_type(self):
        data = {"name": "DNI", "description": "Updated description"}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Updated description")

    def test_update_document_type_invalid_data(self):
        data = {"name": "INVALID"}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_document_type(self):
        doc_type = DocumentType.objects.create(name="LE", description="Test")
        response = self.client.delete(f"/document-types/{doc_type.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_document_type_not_found(self):
        response = self.client.delete("/document-types/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_types_url_exists(self):
        response = self.client.get("/document-types/")
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_types_detail_url_format(self):
        response = self.client.get(f"/document-types/{self.document_type.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_contains_all_fields(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = ["id", "name", "description", "created_at", "updated_at"]
        for field in expected_fields:
            self.assertIn(field, response.data)
