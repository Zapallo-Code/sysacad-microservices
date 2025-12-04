from django.test import TestCase

from app.models import DocumentType
from app.serializers import DocumentTypeSerializer


class DocumentTypeSerializerTest(TestCase):
    def test_valid_data(self):
        data = {"name": "DNI", "description": "Documento Nacional de Identidad"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_choices(self):
        valid_choices = ["DNI", "LC", "LE", "PASAPORTE"]
        for choice in valid_choices:
            data = {"name": choice, "description": f"Test {choice}"}
            serializer = DocumentTypeSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Choice {choice} should be valid")

    def test_invalid_choice(self):
        data = {"name": "INVALID", "description": "Test"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_required(self):
        data = {"description": "Test"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_description_optional(self):
        data = {"name": "DNI"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_description_blank_allowed(self):
        data = {"name": "DNI", "description": ""}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_description_max_length(self):
        data = {"name": "DNI", "description": "a" * 101}
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_description_stripped(self):
        data = {"name": "DNI", "description": "  Test description  "}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["description"], "Test description")

    def test_serialization(self):
        doc_type = DocumentType.objects.create(
            name="DNI", description="Documento Nacional de Identidad"
        )
        serializer = DocumentTypeSerializer(doc_type)
        self.assertEqual(serializer.data["name"], "DNI")
        self.assertEqual(serializer.data["description"], "Documento Nacional de Identidad")
        self.assertIn("id", serializer.data)
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)

    def test_read_only_fields(self):
        data = {
            "name": "DNI",
            "id": 999,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-01T00:00:00Z",
        }
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("created_at", serializer.validated_data)
        self.assertNotIn("updated_at", serializer.validated_data)
