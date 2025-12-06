import pytest

from app.models import DocumentType
from app.services import DocumentTypeService


@pytest.fixture
def document_type(db):
    return DocumentType.objects.create(
        name="DNI", description="Documento Nacional de Identidad"
    )


@pytest.fixture
def document_type_service():
    return DocumentTypeService()


@pytest.mark.django_db
class TestDocumentTypeService:
    def test_create_document_type(self, document_type_service):
        data = {"name": "LC", "description": "Libreta Cívica"}
        doc_type = document_type_service.create(data)
        assert doc_type.name == "LC"
        assert doc_type.description == "Libreta Cívica"
        assert doc_type.id is not None

    def test_find_by_id_existing(self, document_type_service, document_type):
        found = document_type_service.find_by_id(document_type.id)
        assert found is not None
        assert found.name == "DNI"

    def test_find_by_id_not_existing(self, document_type_service):
        found = document_type_service.find_by_id(9999)
        assert found is None

    def test_find_by_name_existing(self, document_type_service, document_type):
        found = document_type_service.find_by_name("DNI")
        assert found is not None
        assert found.id == document_type.id

    def test_find_by_name_not_existing(self, document_type_service):
        found = document_type_service.find_by_name("NONEXISTENT")
        assert found is None

    def test_find_all(self, document_type_service, document_type):
        DocumentType.objects.create(name="LC", description="Libreta Cívica")
        all_types = document_type_service.find_all()
        assert len(all_types) == 2

    def test_update_document_type(self, document_type_service, document_type):
        updated = document_type_service.update(
            document_type.id, {"description": "Updated description"}
        )
        assert updated.description == "Updated description"

    def test_update_non_existing_raises_error(self, document_type_service):
        with pytest.raises(ValueError, match="does not exist"):
            document_type_service.update(9999, {"description": "Test"})

    def test_delete_by_id_existing(self, document_type_service):
        doc_type = DocumentType.objects.create(name="LE", description="Test")
        result = document_type_service.delete_by_id(doc_type.id)
        assert result is True

    def test_delete_by_id_not_existing_raises_error(self, document_type_service):
        with pytest.raises(ValueError, match="does not exist"):
            document_type_service.delete_by_id(9999)
