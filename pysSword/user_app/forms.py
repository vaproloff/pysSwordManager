from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class EditFirstNameForm(UserChangeForm):
    """
    Form class to edit the first name of a user.

    This form class inherits from Django's UserChangeForm and is used to allow users to edit their first name.
    The form contains fields for modifying the first name of the user.

    Attributes:
        Meta (class): Inner class containing metadata for the form.
            - model (User): The model class associated with the form, which is User.
            - fields (list): The list of fields to include in the form, which only includes 'first_name'.
    """

    class Meta:
        model = User
        fields = ['first_name']


class EditLastNameForm(UserChangeForm):
    """
    Form class to edit the last name of a user.

    This form class inherits from Django's UserChangeForm and is used to allow users to edit their last name.
    The form contains fields for modifying the last name of the user.

    Attributes:
        Meta (class): Inner class containing metadata for the form.
            - model (User): The model class associated with the form, which is User.
            - fields (list): The list of fields to include in the form, which only includes 'last_name'.
    """

    class Meta:
        model = User
        fields = ['last_name']
