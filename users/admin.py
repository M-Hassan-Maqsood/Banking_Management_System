from django.contrib import admin
from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "date_joined")
    search_fields = ("first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")
