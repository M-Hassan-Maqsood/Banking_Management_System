from django.db import models


class AccountType(models.TextChoices):
    Saving = "savings", "Savings"
    Current = "current", "Current"
