from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role", "external_id")}),
    )
    list_display = ("username", "email", "role", "external_id", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
