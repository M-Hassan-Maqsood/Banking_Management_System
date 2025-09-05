from django.contrib import admin
from banks.models import Bank, BankBranch


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "swift_code", "is_islamic", "established_date")
    search_fields = ("name", "swift_code")
    list_filter = ("is_islamic",)


@admin.register(BankBranch)
class BankBranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "branch_code", "bank", "address")
    search_fields = ("name", "branch_code", "bank__name")
    list_filter = ("bank",)
