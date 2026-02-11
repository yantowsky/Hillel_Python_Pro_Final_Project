from django.contrib import admin

from .models import Appointment, MedicalRecord


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "scheduled_at", "status", "projectb_conversation_id", "created_at")
    list_filter = ("status", "scheduled_at")
    search_fields = ("patient__username", "doctor__username")


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "diagnosis", "created_at")
    list_filter = ("created_at",)
    search_fields = ("patient__username", "doctor__username", "diagnosis")
