from django import forms
from .models import PasswordEntry


class PasswordEntryForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', required=True,
                               widget=forms.PasswordInput(render_value=True,
                                                          attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    class Meta:
        model = PasswordEntry
        fields = ['title', 'website', 'username', 'password', 'notes']
        labels = {'title': 'Наименование', 'website': 'Веб-сайт',
                  'username': 'Логин', 'notes': 'Заметка'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименование'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Веб-сайт'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст заметки'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.encrypted_password = instance.encrypt_password(self.cleaned_data['password'].encode('utf-8'))

        if commit:
            instance.save()

        return instance


class PasswordEntrySearchForm(forms.Form):
    search_term = forms.CharField(label='Поиск', required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))
