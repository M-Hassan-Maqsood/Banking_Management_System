from django.db import models

from BMS.choices import AccountType, AmountType
from BMS.models import BaseModel


class Account(BaseModel):
    account_number = models.IntegerField()
    account_type = models.CharField(max_length = 55, choices = AccountType.choices)
    balance = models.PositiveIntegerField(default = 0)

    user = models.ForeignKey("users.User", on_delete = models.CASCADE, related_name = "accounts")
    branch = models.ForeignKey("banks.Branch", on_delete = models.CASCADE, related_name = "accounts")

    class Meta:
        db_table = "account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"


class Transaction(BaseModel):
    date = models.DateField()
    amount = models.DecimalField(decimal_places = 2, max_digits = 10)
    type = models.CharField(max_length = 55, choices = AmountType.choices)

    account = models.ForeignKey("accounts.Account", on_delete = models.CASCADE, related_name = "transactions")

    class Meta:
        db_table = "transaction"
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.account} - {self.type} - {self.amount}"
