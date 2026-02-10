from rest_framework import serializers

from .models import Appointment, MedicalRecord


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "patient",
            "doctor",
            "scheduled_at",
            "status",
            "projectb_conversation_id",
            "created_at",
        )
        read_only_fields = ("projectb_conversation_id", "created_at")


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ("id", "patient", "doctor", "diagnosis", "notes", "created_at")
        read_only_fields = ("created_at",)