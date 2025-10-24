from django.contrib import admin

from .models import Student, DocumentType


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_number",
        "full_name",
        "document_number",
        "document_type",
        "birth_date",
        "gender",
        "enrollment_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("gender", "document_type", "enrollment_date")
    search_fields = (
        "first_name",
        "last_name",
        "document_number",
        "student_number",
    )
    ordering = ("last_name", "first_name")
    date_hierarchy = "enrollment_date"
    readonly_fields = ("created_at", "updated_at", "full_name")

    fieldsets = (
        (
            "Información Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "full_name",
                    "birth_date",
                    "gender",
                )
            },
        ),
        (
            "Documentación",
            {
                "fields": (
                    "document_type",
                    "document_number",
                )
            },
        ),
        (
            "Información Académica",
            {
                "fields": (
                    "student_number",
                    "enrollment_date",
                )
            },
        ),
        (
            "Metadatos",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = ("name",)
    search_fields = ("name", "description")
    ordering = ("name",)
