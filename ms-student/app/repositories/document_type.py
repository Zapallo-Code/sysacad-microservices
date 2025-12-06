from django.core.exceptions import ObjectDoesNotExist

from app.models import DocumentType


class DocumentTypeRepository:
    @staticmethod
    def create(document_type_data: dict[str, object]) -> DocumentType:
        document_type = DocumentType(**document_type_data)
        document_type.full_clean()
        document_type.save()
        return document_type

    @staticmethod
    def find_by_id(id: int) -> DocumentType | None:
        try:
            return DocumentType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return DocumentType.objects.all()

    @staticmethod
    def find_by_name(name: str) -> DocumentType | None:
        try:
            return DocumentType.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(document_type: DocumentType) -> DocumentType:
        document_type.full_clean()
        document_type.save()
        return document_type

    @staticmethod
    def delete_by_id(id: int) -> bool:
        document_type = DocumentTypeRepository.find_by_id(id)
        if not document_type:
            return False
        document_type.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return DocumentType.objects.filter(id=id).exists()
