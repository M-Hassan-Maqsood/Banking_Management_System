from django.db import models
from users.models import User
from banks.models import BankBranch


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "accounts")
    bank_branch = models.ForeignKey(BankBranch, on_delete = models.CASCADE, related_name = "accounts")
    account_number = models.CharField(max_length = 20, unique = True)
    ACCOUNT_TYPES = [
        ("savings", "Savings"),
        ("current", "Current"),
                    ]
    account_type = models.CharField(max_length = 10, choices = ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"
