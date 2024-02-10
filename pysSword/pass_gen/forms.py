from django import forms

from pass_gen.models import PasswordGenerationSettings


class PasswordGeneratorForm(forms.ModelForm):
    class Meta:
        model = PasswordGenerationSettings
        fields = [
            'pass_quantity',
            'pass_length',
            'include_digits',
            'include_lowercase',
            'include_uppercase',
            'include_symbols',
            'custom_symbols',
        ]
        labels = {
            'pass_quantity': 'Количество паролей',
            'pass_length': 'Количество символов',
            'include_digits': 'Включить цифры',
            'include_lowercase': 'Включить строчные буквы',
            'include_uppercase': 'Включить заглавные буквы',
            'include_symbols': 'Включить символы',
            'custom_symbols': 'Набор символов',
        }
