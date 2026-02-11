from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_ref",
        "patient_external_id",
        "doctor_external_id",
        "created_by",
        "created_at",
    )
    search_fields = ("external_ref", "patient_external_id", "doctor_external_id")
    list_filter = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "created_at")
    search_fields = ("text",)
    list_filter = ("created_at",)
