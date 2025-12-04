from django.db import models


class DocumentType(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ("DNI", "DNI - Documento Nacional de Identidad"),
        ("LC", "L.C - Libreta Cívica"),
        ("LE", "L.E - Libreta de Enrolamiento"),
        ("PASAPORTE", "Pasaporte"),
    ]

    name = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPE_CHOICES,
        unique=True,
        help_text="Document Type",
    )
    description = models.CharField(
        max_length=100, blank=True, help_text="Document Type Description"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "document_types"
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()

    def __repr__(self):
        return f"<DocumentType: {self.name}>"
