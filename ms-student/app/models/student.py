from datetime import date

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

    specialty_id = models.IntegerField(help_text="Store the specialty ID from the Specialty.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del estudiante"""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int | None:
        """Calcula la edad actual del estudiante"""
        if not self.birth_date:
            return None
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def age_at_date(self, target_date: date) -> int | None:
        """Calcula la edad del estudiante en una fecha específica"""
        if not self.birth_date:
            return None
        age = target_date.year - self.birth_date.year
        if (target_date.month, target_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - Student Number: {self.student_number}"

    def __repr__(self):
        return f"<Student: {self.last_name}, {self.first_name}>"

    class Meta:
        db_table = "students"
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["student_number"]),
            models.Index(fields=["document_number"]),
            models.Index(fields=["last_name", "first_name"]),
        ]
