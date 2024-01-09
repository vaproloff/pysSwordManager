from string import digits, ascii_lowercase, ascii_uppercase, punctuation

from django.utils.crypto import get_random_string


def generate_passwords(pass_quantity, pass_length, include_digits, include_lowercase, include_uppercase,
                       include_symbols, symbols=punctuation):
    all_chars = ''

    if include_digits:
        all_chars += digits
    if include_lowercase:
        all_chars += ascii_lowercase
    if include_uppercase:
        all_chars += ascii_uppercase
    if include_symbols:
        all_chars += symbols

    passwords = set()
    while len(passwords) < pass_quantity:
        passwords.add(get_random_string(pass_length, allowed_chars=all_chars))

    return list(passwords)
