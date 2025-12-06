import logging

from django.core.cache import cache
from django.db import transaction

from app.models import DocumentType
from app.repositories import DocumentTypeRepository

logger = logging.getLogger(__name__)


class DocumentTypeService:
    def __init__(self, repository: DocumentTypeRepository = None):
        """Inicializa el servicio con su repositorio.
        
        Args:
            repository: Repository para tipos de documento (default: DocumentTypeRepository)
        """
        self.repository = repository or DocumentTypeRepository

    @transaction.atomic
    def create(self, document_type_data: dict) -> DocumentType:
        doc_type = self.repository.create(document_type_data)
        # Invalidate cache
        cache.delete("document_types:all")
        return doc_type

    def find_by_id(self, id: int) -> DocumentType | None:
        """Obtiene tipo de documento por ID con caché."""
        cache_key = f"document_type:{id}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"Cache hit for document_type:{id}")
            return cached
        
        doc_type = self.repository.find_by_id(id)
        if doc_type:
            cache.set(cache_key, doc_type, timeout=600)  # 10 minutes
        return doc_type

    def find_by_name(self, name: str) -> DocumentType | None:
        return self.repository.find_by_name(name)

    def find_all(self) -> list[DocumentType]:
        """Obtiene todos los tipos de documento con caché."""
        cache_key = "document_types:all"
        cached = cache.get(cache_key)
        if cached:
            logger.debug("Cache hit for document_types:all")
            return cached
        
        doc_types = list(self.repository.find_all())
        cache.set(cache_key, doc_types, timeout=600)  # 10 minutes
        return doc_types

    def _update_entity_fields(self, entity, data: dict):
        """Actualiza campos de una entidad con los datos proporcionados."""
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        return entity

    @transaction.atomic
    def update(self, id: int, document_type_data: dict) -> DocumentType:
        existing_document_type = self.repository.find_by_id(id)
        if not existing_document_type:
            logger.error(f"Document type with id {id} not found for update")
            raise ValueError(f"Document type with id {id} does not exist")

        self._update_entity_fields(existing_document_type, document_type_data)
        updated = self.repository.update(existing_document_type)
        # Invalidate cache
        cache.delete(f"document_type:{id}")
        cache.delete("document_types:all")
        return updated

    @transaction.atomic
    def delete_by_id(self, id: int) -> bool:
        if not self.repository.exists_by_id(id):
            logger.error(f"Document type with id {id} not found for deletion")
            raise ValueError(f"Document type with id {id} does not exist")
        result = self.repository.delete_by_id(id)
        # Invalidate cache
        cache.delete(f"document_type:{id}")
        cache.delete("document_types:all")
        return result
