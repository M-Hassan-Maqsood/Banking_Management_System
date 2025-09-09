from django.contrib import admin
from banks.models import Bank, Branch


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "established_date",)
    search_fields = ("name", "swift_code",)
    list_filter = ("is_islamic",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "branch_code", "name", "bank")
    search_fields = ("name", "branch_code",)
    list_filter = ("bank",)
