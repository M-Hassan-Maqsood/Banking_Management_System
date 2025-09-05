from django.contrib import admin
from accounts.models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_number", "user", "bank_branch", "account_type", "balance", "is_active")
    search_fields = ("account_number", "user__username", "bank_branch__name")
    list_filter = ("account_type", "is_active", "bank_branch")
