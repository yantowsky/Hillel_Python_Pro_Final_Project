from django.conf import settings
from django.db import models


class Conversation(models.Model):
    """
    Conversation прив'язана до:
    - external_ref: ID Appointment з ProjectA
    - patient_external_id / doctor_external_id: ID користувачів з ProjectA
    """
    external_ref = models.PositiveIntegerField(unique=True)
    patient_external_id = models.PositiveIntegerField()
    doctor_external_id = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_conversations",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Conversation #{self.pk} ext_ref={self.external_ref}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Message #{self.pk} conv={self.conversation_id}"
