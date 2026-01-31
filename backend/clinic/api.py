from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Appointment

User = get_user_model()


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(role=User.Role.DOCTOR).order_by("username")


class AppointmentSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source="patient.username", read_only=True)
    doctor_username = serializers.CharField(source="doctor.username", read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.Role.DOCTOR))

    class Meta:
        model = Appointment
        fields = (
            "id",
            "patient",
            "patient_username",
            "doctor",
            "doctor_username",
            "starts_at",
            "status",
            "video_room_url",
            "created_at",
        )
        read_only_fields = ("patient", "status", "created_at", "video_room_url")

    def validate_doctor(self, value):
        if value.role != User.Role.DOCTOR:
            raise serializers.ValidationError("Selected user is not a doctor.")
        return value


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.DOCTOR:
            return Appointment.objects.filter(doctor=user).order_by("-starts_at")
        return Appointment.objects.filter(patient=user).order_by("-starts_at")

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
