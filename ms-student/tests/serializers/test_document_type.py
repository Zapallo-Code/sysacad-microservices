from django.test import TestCase
from app.serializers import DocumentTypeSerializer
from app.models import DocumentType


class DocumentTypeSerializerTest(TestCase):
    """Tests for DocumentTypeSerializer."""

    def test_valid_data(self):
        """Test serializer with valid data."""
        data = {"name": "DNI", "description": "Documento Nacional de Identidad"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_choices(self):
        """Test all valid document type choices."""
        valid_choices = ["DNI", "LC", "LE", "PASAPORTE"]
        for choice in valid_choices:
            data = {"name": choice, "description": f"Test {choice}"}
            serializer = DocumentTypeSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Choice {choice} should be valid")

    def test_invalid_choice(self):
        """Test serializer with invalid choice."""
        data = {"name": "INVALID", "description": "Test"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_required(self):
        """Test that name is required."""
        data = {"description": "Test"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_description_optional(self):
        """Test that description is optional."""
        data = {"name": "DNI"}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_description_blank_allowed(self):
        """Test that description can be blank."""
        data = {"name": "DNI", "description": ""}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_description_max_length(self):
        """Test description max length validation."""
        data = {"name": "DNI", "description": "a" * 101}
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_description_stripped(self):
        """Test that description is stripped."""
        data = {"name": "DNI", "description": "  Test description  "}
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["description"], "Test description")

    def test_serialization(self):
        """Test serializing a DocumentType instance."""
        doc_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
        )
        serializer = DocumentTypeSerializer(doc_type)
        self.assertEqual(serializer.data["name"], "DNI")
        self.assertEqual(serializer.data["description"], "Documento Nacional de Identidad")
        self.assertIn("id", serializer.data)
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)

    def test_read_only_fields(self):
        """Test that read_only_fields are not writable."""
        data = {
            "name": "DNI",
            "id": 999,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2020-01-01T00:00:00Z"
        }
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("created_at", serializer.validated_data)
        self.assertNotIn("updated_at", serializer.validated_data)
