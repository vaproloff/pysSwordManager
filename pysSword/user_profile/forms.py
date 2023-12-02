from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User


class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
