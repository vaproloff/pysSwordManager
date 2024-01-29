from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class EditFirstNameForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name']


class EditLastNameForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['last_name']
