from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from core.models import Appointment
from core.tasks import create_projectb_conversation_for_appointment


class ProjectBIntegrationTests(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user(username="patient1", password="x", role=User.Role.PATIENT)
        self.doctor = User.objects.create_user(username="doctor1", password="x", role=User.Role.DOCTOR)

        self.appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            scheduled_at=timezone.now(),
            status=Appointment.Status.REQUESTED,
        )

    @patch("core.projectb_client.requests.post")
    def test_task_creates_conversation_and_saves_conversation_id(self, post: Mock):
        """
        Мокаємо 2 HTTP виклики:
        1) POST /api/auth/token/ -> повертає access
        2) POST /api/telemed/conversations/ -> повертає {"id": 123}
        """
        token_resp = Mock()
        token_resp.raise_for_status = Mock()
        token_resp.json = Mock(return_value={"access": "<ACCESS_TOKEN>"})

        conv_resp = Mock()
        conv_resp.raise_for_status = Mock()
        conv_resp.json = Mock(return_value={"id": 123})

        post.side_effect = [token_resp, conv_resp]

        conversation_id = create_projectb_conversation_for_appointment.run(self.appt.id)

        self.assertEqual(conversation_id, "123")

        self.appt.refresh_from_db()
        self.assertEqual(self.appt.projectb_conversation_id, "123")

        self.assertEqual(post.call_count, 2)