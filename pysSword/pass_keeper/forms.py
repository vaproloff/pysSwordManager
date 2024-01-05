from django import forms
from .models import PasswordEntry


class PasswordEntryForm(forms.ModelForm):
    class Meta:
        model = PasswordEntry
        fields = ['title', 'username', 'password', 'notes', 'website']


class PasswordEntrySearchForm(forms.Form):
    search_term = forms.CharField(label='Search', required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Enter search term'}))
