from rest_framework.permissions import BasePermission

from accounts.models import User
from .models import Conversation


class IsConversationParticipantOrAdmin(BasePermission):
    """
    Доступ до Conversation/Message:
    - ADMIN: все
    - інші: тільки якщо їхній external_id збігається з patient_external_id або doctor_external_id
    """

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role == User.Role.ADMIN:
            return True

        if user.external_id is None:
            return False

        if isinstance(obj, Conversation):
            conv = obj
        else:
            conv = getattr(obj, "conversation", None)

        if conv is None:
            return False

        return user.external_id in (conv.patient_external_id, conv.doctor_external_id)