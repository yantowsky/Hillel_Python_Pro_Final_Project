from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from .models import Appointment, MedicalRecord
from .permissions import IsOwnerPatientOrOwnerDoctorOrAdmin
from .serializers import AppointmentSerializer, MedicalRecordSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated, IsOwnerPatientOrOwnerDoctorOrAdmin)

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.all().order_by("-created_at")

        if user.role == User.Role.ADMIN:
            return qs
        if user.role == User.Role.PATIENT:
            return qs.filter(patient_id=user.id)
        if user.role == User.Role.DOCTOR:
            return qs.filter(doctor_id=user.id)

        return qs.none()


class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = (IsAuthenticated, IsOwnerPatientOrOwnerDoctorOrAdmin)

    def get_queryset(self):
        user = self.request.user
        qs = MedicalRecord.objects.all().order_by("-created_at")

        if user.role == User.Role.ADMIN:
            return qs
        if user.role == User.Role.PATIENT:
            return qs.filter(patient_id=user.id)
        if user.role == User.Role.DOCTOR:
            return qs.filter(doctor_id=user.id)

        return qs.none()
