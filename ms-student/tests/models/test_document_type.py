from django.test import TestCase
from django.db import IntegrityError
from app.models import DocumentType


class DocumentTypeModelTest(TestCase):

    def setUp(self):
        """Set up test data."""
        self.document_type = DocumentType.objects.create(
            name="DNI",
            description="Documento Nacional de Identidad"
        )

    def test_create_document_type(self):
        self.assertEqual(self.document_type.name, "DNI")
        self.assertEqual(self.document_type.description, "Documento Nacional de Identidad")

    def test_str_representation(self):
        expected = "DNI - Documento Nacional de Identidad"
        self.assertEqual(str(self.document_type), expected)

    def test_repr_representation(self):
        expected = "<DocumentType: DNI>"
        self.assertEqual(repr(self.document_type), expected)

    def test_name_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            DocumentType.objects.create(
                name="DNI",
                description="Duplicate DNI"
            )

    def test_description_blank_allowed(self):
        doc_type = DocumentType.objects.create(
            name="LC",
            description=""
        )
        self.assertEqual(doc_type.description, "")

    def test_valid_document_type_choices(self):
        valid_choices = ["DNI", "LC", "LE", "PASAPORTE"]
        for choice in valid_choices:
            if choice != "DNI":
                doc_type = DocumentType.objects.create(
                    name=choice,
                    description=f"Test {choice}"
                )
                self.assertEqual(doc_type.name, choice)

    def test_created_at_auto_now_add(self):
        self.assertIsNotNone(self.document_type.created_at)

    def test_updated_at_auto_now(self):
        self.assertIsNotNone(self.document_type.updated_at)

    def test_meta_db_table(self):
        self.assertEqual(DocumentType._meta.db_table, "document_types")

    def test_meta_verbose_name(self):
        self.assertEqual(DocumentType._meta.verbose_name, "Document Type")
        self.assertEqual(DocumentType._meta.verbose_name_plural, "Document Types")

    def test_meta_ordering(self):
        self.assertEqual(DocumentType._meta.ordering, ["name"])

    def test_get_name_display(self):
        self.assertEqual(
            self.document_type.get_name_display(),
            "DNI - Documento Nacional de Identidad"
        )
