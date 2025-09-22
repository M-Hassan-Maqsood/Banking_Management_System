from django.db import models


class AccountType(models.TextChoices):
    SAVING = "saving", "Saving"
    CURRENT = "current", "Current"


class AmountType(models.TextChoices):
    Deposit = "deposit", "Deposit",
    Withdrawal = "withdrawal", "Withdrawal"
