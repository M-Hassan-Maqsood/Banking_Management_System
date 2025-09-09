from django.contrib.auth.models import AbstractUser
from django.db import models

from BMS.models import BaseModel


class User(AbstractUser, BaseModel):
    phone = models.CharField(max_length = 15)
    date_of_birth = models.DateField()

    REQUIRED_FIELDS = ["phone", "date_of_birth"]

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.id} - {self.username}"
