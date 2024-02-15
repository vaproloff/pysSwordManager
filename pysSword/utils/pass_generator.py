from string import digits, ascii_lowercase, ascii_uppercase, punctuation

from django.utils.crypto import get_random_string


def generate_passwords(pass_quantity=1, pass_length=12,
                       include_digits=True, include_lowercase=True, include_uppercase=True, include_symbols=True,
                       custom_symbols=punctuation):
    """
    Function to generate random passwords based on the specified parameters.

    The function constructs a string containing all characters to be used in generating passwords based on the
    specified parameters. It then generates random strings of the specified length using the characters and
    ensures uniqueness of passwords. Finally, it returns a list of generated passwords.

    :param pass_quantity: Number of passwords to generate (default is 1).
    :param pass_length: Length of each password (default is 12).
    :param include_digits: Whether to include digits in the passwords (default is True).
    :param include_lowercase: Whether to include lowercase letters in the passwords (default is True).
    :param include_uppercase: Whether to include uppercase letters in the passwords (default is True).
    :param include_symbols: Whether to include symbols in the passwords (default is True).
    :param custom_symbols: Custom symbols to include in the passwords (default is string.punctuation).
    :return: List of generated passwords.
    """
    all_chars = ''

    if include_digits:
        all_chars += digits
    if include_lowercase:
        all_chars += ascii_lowercase
    if include_uppercase:
        all_chars += ascii_uppercase
    if include_symbols:
        all_chars += custom_symbols

    passwords = set()
    while len(passwords) < pass_quantity:
        passwords.add(get_random_string(pass_length, allowed_chars=all_chars))

    return list(passwords)
