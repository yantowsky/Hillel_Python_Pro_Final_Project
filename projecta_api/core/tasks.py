from celery import shared_task
from django.db import transaction

from .models import Appointment
from .projectb_client import get_projectb_client


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def create_projectb_conversation_for_appointment(self, appointment_id: int) -> str:
    """
    1) Беремо Appointment з ProjectA
    2) Логінимось у ProjectB (JWT)
    3) Створюємо Conversation (external_ref = appointment_id)
    4) Записуємо conversation_id в appointment.projectb_conversation_id
    """
    try:
        appt = Appointment.objects.select_related("patient", "doctor").get(pk=appointment_id)

        # Якщо вже створили conversation — не дублюємо
        if appt.projectb_conversation_id:
            return appt.projectb_conversation_id

        client = get_projectb_client()

        access = client.get_access_token()
        conv = client.create_conversation(
            access_token=access,
            external_ref=appt.id,
            patient_external_id=appt.patient_id,
            doctor_external_id=appt.doctor_id,
        )

        conversation_id = str(conv["id"])

        with transaction.atomic():
            appt.projectb_conversation_id = conversation_id
            appt.save(update_fields=["projectb_conversation_id"])

        return conversation_id
    except Exception as exc:
        raise self.retry(exc=exc)