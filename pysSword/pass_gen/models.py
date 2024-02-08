from string import punctuation

from django.db import models
from django.contrib.auth.models import User, AnonymousUser


class PasswordGenerationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=AnonymousUser)
    pass_quantity = models.IntegerField(default=10)
    pass_length = models.IntegerField(default=12)
    include_digits = models.BooleanField(default=True)
    include_lowercase = models.BooleanField(default=True)
    include_uppercase = models.BooleanField(default=True)
    include_symbols = models.BooleanField(default=True)
    custom_symbols = models.CharField(max_length=50, blank=True, null=True, default=punctuation)
