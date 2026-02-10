from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    external_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="ID of this user in ProjectA",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
