from string import digits, ascii_lowercase, ascii_uppercase, punctuation

from django.utils.crypto import get_random_string


def generate_passwords(pass_quantity=1, pass_length=12,
                       include_digits=True, include_lowercase=True, include_uppercase=True, include_symbols=True,
                       custom_symbols=punctuation):
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
