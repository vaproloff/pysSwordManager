from django import forms
from .models import PasswordEntry


class PasswordEntryForm(forms.ModelForm):
    """
    Form class for creating or editing a password entry.

    This form class inherits from Django's ModelForm and is used to create or edit a password entry.
    It includes fields for the title, website, username, password, and notes of the password entry.

    Attributes:
        password (CharField): Field for the password, rendered as a password input widget.
            - label (str): Label for the password field.
            - required (bool): Indicates whether the password field is required.
            - widget (PasswordInput): Widget for rendering the password input field.
            - attrs (dict): Additional attributes for the password input widget, including CSS classes and placeholder.

    Methods:
        save(self, commit=True): Method to save the form data to the corresponding model instance.
            - commit (bool): Flag indicating whether to save the instance to the database immediately.

    Meta (class): Inner class containing metadata for the form.
        - model (PasswordEntry): The model class associated with the form, which is PasswordEntry.
        - fields (list): The list of fields to include in the form, including 'title', 'website', 'username',
                         'password', and 'notes'.
        - labels (dict): Custom labels for form fields.
        - widgets (dict): Custom widgets for form fields.

    """
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
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин или email'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст заметки'}),
        }

    def save(self, commit=True):
        """
        Save method to encrypt the password and save the form data to the corresponding model instance.

        This method overrides the parent class method to encrypt the password before saving it to the database.
        It encrypts the password using the `encrypt_password` method of the PasswordEntry model.
        If the `commit` parameter is True, the instance is saved to the database.

        :param commit: Flag indicating whether to save the instance to the database immediately.
        :return: The saved instance.
        """
        instance = super().save(commit=False)
        instance.encrypted_password = instance.encrypt_password(self.cleaned_data['password'].encode('utf-8'))

        if commit:
            instance.save()

        return instance
