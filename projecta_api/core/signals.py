from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Appointment
from .tasks import create_projectb_conversation_for_appointment


@receiver(post_save, sender=Appointment)
def appointment_post_save(sender, instance: Appointment, created: bool, **kwargs):
    """
    Запускаємо інтеграцію тільки при створенні Appointment.
    Додатково перевіряємо, що conversation ще не створена,
    щоб уникнути дубляжу.
    """
    if not created:
        return

    if instance.projectb_conversation_id:
        return

    create_projectb_conversation_for_appointment.delay(instance.id)