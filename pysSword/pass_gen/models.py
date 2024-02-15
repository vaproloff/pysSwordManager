from string import punctuation

from django.db import models
from django.contrib.auth.models import User, AnonymousUser


class PasswordGenerationSettings(models.Model):
    """
    Model class representing password generation settings for users.

    This model class defines the settings used for generating passwords for users. It includes fields such as the
    user associated with the settings, the quantity of passwords to generate, the length of each password, and
    options to include digits, lowercase letters, uppercase letters, and symbols in the generated passwords.
    Additionally, users can specify custom symbols to include in the passwords.

    Attributes:
        user (OneToOneField): One-to-one relationship with the User model, representing the user associated with
                              the settings.
        pass_quantity (IntegerField): Number of passwords to generate (default is 10).
        pass_length (IntegerField): Length of each password (default is 12).
        include_digits (BooleanField): Indicates whether to include digits in the generated passwords (default is True).
        include_lowercase (BooleanField): Indicates whether to include lowercase letters in the generated passwords
                                           (default is True).
        include_uppercase (BooleanField): Indicates whether to include uppercase letters in the generated passwords
                                           (default is True).
        include_symbols (BooleanField): Indicates whether to include symbols in the generated passwords
                                           (default is True).
        custom_symbols (CharField): Custom symbols to include in the generated passwords
                                           (optional, default is string.punctuation).

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=AnonymousUser)
    pass_quantity = models.IntegerField(default=10)
    pass_length = models.IntegerField(default=12)
    include_digits = models.BooleanField(default=True)
    include_lowercase = models.BooleanField(default=True)
    include_uppercase = models.BooleanField(default=True)
    include_symbols = models.BooleanField(default=True)
    custom_symbols = models.CharField(max_length=50, blank=True, null=True, default=punctuation)
