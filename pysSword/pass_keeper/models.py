from django.db import models
from user_app.models import User


class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=255)
    password = models.TextField()
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
