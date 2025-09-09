from django.contrib import admin
from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "phone")
    search_fields = ("username", "email", "phone", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")
