from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.models import DocumentType


class DocumentTypeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.document_type = DocumentType.objects.create(
            name="DNI", description="Documento Nacional de Identidad"
        )
        self.list_url = "/api/v1/document-types/"
        self.detail_url = f"/api/v1/document-types/{self.document_type.id}/"

    def test_list_document_types(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_document_type(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "DNI")

    def test_retrieve_document_type_not_found(self):
        response = self.client.get("/api/v1/document-types/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Document type not found")

    def test_response_contains_all_fields(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = ["id", "name", "description", "created_at", "updated_at"]
        for field in expected_fields:
            self.assertIn(field, response.data)
