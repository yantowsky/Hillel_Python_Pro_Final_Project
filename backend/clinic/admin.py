from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "starts_at", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("patient__username", "doctor__username")
