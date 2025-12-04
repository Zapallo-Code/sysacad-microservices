from rest_framework import serializers

from app.models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(
        choices=DocumentType.DOCUMENT_TYPE_CHOICES,
        required=True,
        error_messages={
            "required": "Document type name is required.",
            "invalid_choice": "Invalid document type choice.",
        },
    )

    description = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        error_messages={
            "max_length": "Description must not exceed 100 characters.",
        },
    )

    def validate_description(self, value):
        if value:
            return value.strip()
        return value

    class Meta:
        model = DocumentType
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
