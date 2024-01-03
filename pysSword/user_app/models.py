from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    is_staff = None
    is_superuser = None

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
