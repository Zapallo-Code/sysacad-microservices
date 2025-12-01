from django.test import TestCase
from app.models import DocumentType
from app.repositories import DocumentTypeRepository


class DocumentTypeRepositoryTest(TestCase):
    """Tests for DocumentTypeRepository."""

    def setUp(self):
        """Set up test data."""
        self.document_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
        )

    def test_create_document_type(self):
        """Test creating a document type."""
        data = {"name": "LC", "description": "Libreta Cívica"}
        doc_type = DocumentTypeRepository.create(data)
        self.assertEqual(doc_type.name, "LC")
        self.assertEqual(doc_type.description, "Libreta Cívica")
        self.assertIsNotNone(doc_type.id)

    def test_find_by_id_existing(self):
        """Test finding an existing document type by id."""
        found = DocumentTypeRepository.find_by_id(self.document_type.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "DNI")

    def test_find_by_id_not_existing(self):
        """Test finding a non-existing document type by id."""
        found = DocumentTypeRepository.find_by_id(9999)
        self.assertIsNone(found)

    def test_find_all(self):
        """Test finding all document types."""
        DocumentType.objects.create(name="LC", description="Libreta Cívica")
        all_types = DocumentTypeRepository.find_all()
        self.assertEqual(len(all_types), 2)

    def test_find_by_name_existing(self):
        """Test finding a document type by name."""
        found = DocumentTypeRepository.find_by_name("DNI")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, self.document_type.id)

    def test_find_by_name_not_existing(self):
        """Test finding a non-existing document type by name."""
        found = DocumentTypeRepository.find_by_name("NONEXISTENT")
        self.assertIsNone(found)

    def test_update_document_type(self):
        """Test updating a document type."""
        self.document_type.description = "Updated description"
        updated = DocumentTypeRepository.update(self.document_type)
        self.assertEqual(updated.description, "Updated description")

    def test_delete_by_id_existing(self):
        """Test deleting an existing document type."""
        doc_type = DocumentType.objects.create(name="LE", description="Test")
        result = DocumentTypeRepository.delete_by_id(doc_type.id)
        self.assertTrue(result)
        self.assertIsNone(DocumentTypeRepository.find_by_id(doc_type.id))

    def test_delete_by_id_not_existing(self):
        """Test deleting a non-existing document type."""
        result = DocumentTypeRepository.delete_by_id(9999)
        self.assertFalse(result)

    def test_exists_by_id_true(self):
        """Test exists_by_id returns True for existing document type."""
        self.assertTrue(DocumentTypeRepository.exists_by_id(self.document_type.id))

    def test_exists_by_id_false(self):
        """Test exists_by_id returns False for non-existing document type."""
        self.assertFalse(DocumentTypeRepository.exists_by_id(9999))

    def test_count(self):
        """Test counting document types."""
        initial_count = DocumentTypeRepository.count()
        DocumentType.objects.create(name="LC", description="Test")
        self.assertEqual(DocumentTypeRepository.count(), initial_count + 1)
