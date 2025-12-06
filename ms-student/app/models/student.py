from datetime import date

from django.core.validators import MinValueValidator
from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    document_number = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
    )
    student_number = models.IntegerField(unique=True)
    enrollment_date = models.DateField()

    document_type = models.ForeignKey(
        "DocumentType",
        on_delete=models.PROTECT,
        related_name="students",
    )

    specialty_id = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Store the specialty ID from the Specialty microservice."
    )

    # Soft delete fields
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "students"
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["student_number"]),
            models.Index(fields=["document_number"]),
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["specialty_id"]),
            models.Index(fields=["is_active", "deleted_at"]),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - Student Number: {self.student_number}"

    def __repr__(self):
        return f"<Student: {self.last_name}, {self.first_name}>"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def calculate_age(birth_date: date, reference_date: date = None) -> int | None:
        if not birth_date:
            return None
        if reference_date is None:
            reference_date = date.today()
        age = reference_date.year - birth_date.year
        if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
