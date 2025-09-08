from django.contrib import admin
from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_number", "user", "bank_branch", "balance")
    search_fields = ("account_number", "user__username", "bank_branch__name")
    list_filter = ("account_type", "is_active", "bank_branch")
