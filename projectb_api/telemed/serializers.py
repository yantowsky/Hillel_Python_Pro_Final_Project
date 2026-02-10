from rest_framework import serializers

from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = (
            "id",
            "external_ref",
            "patient_external_id",
            "doctor_external_id",
            "created_by",
            "created_at",
        )
        read_only_fields = ("created_by", "created_at")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "conversation", "sender", "text", "created_at")
        read_only_fields = ("sender", "created_at")