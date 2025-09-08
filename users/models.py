from django.contrib.auth.models import AbstractUser
from django.db import models

from BMS.models import BaseModel


class User(AbstractUser, BaseModel):
    phone = models.CharField(max_length = 15)
    date_of_birth = models.DateField(null = True)

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{id} - {self.username}"
