from django import forms
from string import punctuation


class PasswordGeneratorForm(forms.Form):
    pass_quantity = forms.IntegerField(label='Количество паролей', initial=10, min_value=1, max_value=100)
    pass_length = forms.IntegerField(label='Количество символов', initial=12, min_value=1, max_value=100)
    include_digits = forms.BooleanField(label='Включить цифры', initial=True, required=False)
    include_lowercase = forms.BooleanField(label='Включить прописные буквы', initial=True, required=False)
    include_uppercase = forms.BooleanField(label='Включить заглавные буквы', initial=True, required=False)
    include_symbols = forms.BooleanField(label='Включить символы', initial=True, required=False)
    custom_symbols = forms.CharField(label='Символы', initial=punctuation, max_length=50,
                                     required=False)
