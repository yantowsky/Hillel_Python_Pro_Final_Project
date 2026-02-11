from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from .models import Conversation, Message
from .permissions import IsConversationParticipantOrAdmin
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = (IsAuthenticated, IsConversationParticipantOrAdmin)

    def get_queryset(self):
        user = self.request.user
        qs = Conversation.objects.all().order_by("-created_at")

        if user.role == User.Role.ADMIN:
            return qs

        if user.external_id is None:
            return qs.none()

        return qs.filter(patient_external_id=user.external_id) | qs.filter(doctor_external_id=user.external_id)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsConversationParticipantOrAdmin)

    def _get_conversation(self) -> Conversation:
        conversation_id = self.kwargs.get("conversation_pk")
        conv = get_object_or_404(Conversation, pk=conversation_id)

        # Перевіряємо доступ саме до Conversation (учасник або ADMIN)
        self.check_object_permissions(self.request, conv)
        return conv

    def get_queryset(self):
        conv = self._get_conversation()
        return (
            Message.objects.select_related("conversation", "sender")
            .filter(conversation=conv)
            .order_by("created_at")
        )

    def perform_create(self, serializer):
        conv = self._get_conversation()
        serializer.save(conversation=conv, sender=self.request.user)
