from django.db import models

from BMS.base_models import BaseModel


class Bank(BaseModel):
    name = models.CharField(max_length = 100)
    swift_code = models.CharField(max_length = 16)
    is_islamic = models.BooleanField(default = False)
    established_date = models.DateField()

    class Meta:
        db_table = "bank"
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    def __str__(self):
        return f"{id} - {self.name}"


class Branch(BaseModel):
    name = models.CharField(max_length = 100)
    branch_code = models.CharField(max_length = 16)
    address = models.TextField(blank = True)

    bank = models.ForeignKey("banks.Bank", on_delete=models.CASCADE, related_name="branches")

    class Meta:
        db_table = "branch"
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return f"{id} - {self.name}"
