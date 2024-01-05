from django import forms
from .models import PasswordEntry


class PasswordEntryForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = PasswordEntry
        fields = ['title', 'username', 'password', 'notes', 'website']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.encrypted_password = instance.encrypt_password(self.cleaned_data['password'].encode('utf-8'))

        if commit:
            instance.save()

        return instance


class PasswordEntrySearchForm(forms.Form):
    search_term = forms.CharField(label='Search', required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Enter search term'}))


class PasswordEditEntryForm(forms.ModelForm):
    password = forms.CharField(label='Password', required=True, widget=forms.TextInput())

    class Meta:
        model = PasswordEntry
        fields = ['title', 'username', 'password', 'notes', 'website']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.encrypted_password = instance.encrypt_password(self.cleaned_data['password'].encode('utf-8'))

        if commit:
            instance.save()

        return instance
