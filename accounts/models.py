from django.db import models

from BMS.choices import AccountType
from BMS.models import BaseModel


class Account(BaseModel):
    account_number = models.IntegerField()
    account_type = models.CharField(max_length = 55, choices=AccountType.choices)
    balance = models.PositiveIntegerField(default = 0)

    user = models.ForeignKey("users.User", on_delete = models.CASCADE, related_name = "customer_accounts")
    branch = models.ForeignKey("banks.Branch", on_delete = models.CASCADE, related_name = "branch_accounts")

    class Meta:
        db_table = "account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"
