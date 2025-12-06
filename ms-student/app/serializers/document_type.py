from rest_framework import serializers

from app.models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(choices=DocumentType.DOCUMENT_TYPE_CHOICES)
    description = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_description(self, value):
        return value.strip() if value else value

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
