from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django import forms

from .models import User


class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']


class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True}),
        required=True,
    )

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
