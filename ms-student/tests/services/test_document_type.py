from django.test import TestCase
from app.models import DocumentType
from app.services import DocumentTypeService


class DocumentTypeServiceTest(TestCase):
    """Tests for DocumentTypeService."""

    def setUp(self):
        """Set up test data."""
        self.document_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
        )

    def test_create_document_type(self):
        """Test creating a document type through service."""
        data = {"name": "LC", "description": "Libreta Cívica"}
        doc_type = DocumentTypeService.create(data)
        self.assertEqual(doc_type.name, "LC")
        self.assertEqual(doc_type.description, "Libreta Cívica")
        self.assertIsNotNone(doc_type.id)

    def test_find_by_id_existing(self):
        """Test finding an existing document type by id."""
        found = DocumentTypeService.find_by_id(self.document_type.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "DNI")

    def test_find_by_id_not_existing(self):
        """Test finding a non-existing document type by id."""
        found = DocumentTypeService.find_by_id(9999)
        self.assertIsNone(found)

    def test_find_by_name_existing(self):
        """Test finding a document type by name."""
        found = DocumentTypeService.find_by_name("DNI")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, self.document_type.id)

    def test_find_by_name_not_existing(self):
        """Test finding a non-existing document type by name."""
        found = DocumentTypeService.find_by_name("NONEXISTENT")
        self.assertIsNone(found)

    def test_find_all(self):
        """Test finding all document types."""
        DocumentType.objects.create(name="LC", description="Libreta Cívica")
        all_types = DocumentTypeService.find_all()
        self.assertEqual(len(all_types), 2)

    def test_update_document_type(self):
        """Test updating a document type."""
        updated = DocumentTypeService.update(
            self.document_type.id,
            {"description": "Updated description"}
        )
        self.assertEqual(updated.description, "Updated description")

    def test_update_non_existing_raises_error(self):
        """Test updating a non-existing document type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            DocumentTypeService.update(9999, {"description": "Test"})
        self.assertIn("does not exist", str(context.exception))

    def test_delete_by_id_existing(self):
        """Test deleting an existing document type."""
        doc_type = DocumentType.objects.create(name="LE", description="Test")
        result = DocumentTypeService.delete_by_id(doc_type.id)
        self.assertTrue(result)

    def test_delete_by_id_not_existing_raises_error(self):
        """Test deleting a non-existing document type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            DocumentTypeService.delete_by_id(9999)
        self.assertIn("does not exist", str(context.exception))
