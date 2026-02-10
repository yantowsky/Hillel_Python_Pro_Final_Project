from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

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

        return qs.filter(
            patient_external_id=user.external_id
        ) | qs.filter(
            doctor_external_id=user.external_id
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsConversationParticipantOrAdmin)

    def get_queryset(self):
        qs = Message.objects.select_related("conversation").all().order_by("created_at")

        conversation_id = self.kwargs.get("conversation_pk")
        if conversation_id:
            qs = qs.filter(conversation_id=conversation_id)

        # Важливо: object-level permission відпрацює на retrieve,
        # але для list/create ми руками відфільтруємо по доступних conversation
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return qs

        if user.external_id is None:
            return qs.none()

        allowed_conversations = Conversation.objects.filter(
            patient_external_id=user.external_id
        ) | Conversation.objects.filter(
            doctor_external_id=user.external_id
        )

        return qs.filter(conversation__in=allowed_conversations)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
