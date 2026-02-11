from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from telemed.models import Conversation, Message


class TelemedMessagesApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_test",
            password="testpass123",
            role=User.Role.ADMIN,
            is_active=True,
        )

        token_url = reverse("token_obtain_pair")
        resp = self.client.post(
            token_url,
            {"username": "admin_test", "password": "testpass123"},
            format="json",
        )
        assert resp.status_code == 200, resp.data
        self.access = resp.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

        self.conversation = Conversation.objects.create(
            external_ref=1,
            patient_external_id=1,
            doctor_external_id=2,
            created_by=self.admin,
        )

    def test_create_message_returns_201_and_sets_sender(self):
        url = f"/api/telemed/conversations/{self.conversation.id}/messages/"
        resp = self.client.post(url, {"text": "Hello"}, format="json")

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["text"], "Hello")

        msg = Message.objects.get(id=resp.data["id"])
        self.assertEqual(msg.sender_id, self.admin.id)
        self.assertEqual(msg.conversation_id, self.conversation.id)

    def test_list_messages_returns_200(self):
        Message.objects.create(conversation=self.conversation, sender=self.admin, text="One")
        Message.objects.create(conversation=self.conversation, sender=self.admin, text="Two")

        url = f"/api/telemed/conversations/{self.conversation.id}/messages/"
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(resp.data[0]["text"], "One")
        self.assertEqual(resp.data[1]["text"], "Two")