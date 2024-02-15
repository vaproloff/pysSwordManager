from django import forms

from pass_gen.models import PasswordGenerationSettings


class PasswordGeneratorForm(forms.ModelForm):
    """
    Form class for configuring password generation settings.

    This form class allows users to configure settings for generating passwords. It provides fields for specifying
    the quantity of passwords to generate, the length of each password, whether to include digits, lowercase letters,
    uppercase letters, symbols, and custom symbols for password generation.

    Attributes:
        Meta (class): Inner class containing metadata for the form.
            - model (PasswordGenerationSettings): The model class associated with the form, which is
                                                  PasswordGenerationSettings.
            - fields (list): The list of fields to include in the form, including 'pass_quantity', 'pass_length',
                             'include_digits', 'include_lowercase', 'include_uppercase', 'include_symbols', and
                             'custom_symbols'.
            - labels (dict): Custom labels for form fields.
    """

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
