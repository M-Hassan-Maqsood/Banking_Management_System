from django.contrib import admin
from accounts.models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_number", "user", "is_active", "account_type", "branch")
    search_fields = ("account_number",)
    list_filter = ("account_type", "is_active", "branch",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "date", "amount", "type")
    search_fields = ("account",)
    list_filter = ("type",)
