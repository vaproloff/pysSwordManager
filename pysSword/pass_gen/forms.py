from django import forms
from string import punctuation


class PasswordGeneratorForm(forms.Form):
    pass_quantity = forms.IntegerField(label='Passwords Quantity', initial=10, min_value=1, max_value=100)
    pass_length = forms.IntegerField(label='Password Length', initial=12, min_value=1, max_value=100)
    include_digits = forms.BooleanField(label='Include Digits', initial=True, required=False)
    include_lowercase = forms.BooleanField(label='Include Lowercase Letters', initial=True, required=False)
    include_uppercase = forms.BooleanField(label='Include Uppercase Letters', initial=True, required=False)
    include_symbols = forms.BooleanField(label='Include Symbols', initial=True, required=False)
    custom_symbols = forms.CharField(label='Custom Symbols', initial=punctuation, max_length=50, required=False)
