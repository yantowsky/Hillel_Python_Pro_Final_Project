from django.conf import settings
from django.db import models


class Appointment(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.REQUESTED,
    )

    projectb_conversation_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Conversation id returned by ProjectB",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Appointment #{self.pk} patient={self.patient_id} doctor={self.doctor_id}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_records",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_medical_records",
    )

    diagnosis = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"MedicalRecord #{self.pk} patient={self.patient_id} doctor={self.doctor_id}"
