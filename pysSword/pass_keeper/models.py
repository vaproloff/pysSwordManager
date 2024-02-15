import logging

from django.contrib.auth.models import User
from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

logger = logging.getLogger('app')


class PasswordEntry(models.Model):
    """
    Model class representing a password entry.

    This model class defines the structure of a password entry, including fields for the user, title, website,
    username, encrypted_password, notes, date_created, and last_updated.

    Attributes:
        user (ForeignKey): Foreign key relationship with the User model, representing the user associated with
                           the password entry.
        title (CharField): Field for the title of the password entry.
        website (URLField): Field for the website associated with the password entry (optional).
        username (CharField): Field for the username or identifier associated with the password entry.
        encrypted_password (BinaryField): Field for the encrypted password.
        notes (TextField): Field for additional notes or comments about the password entry (optional).
        date_created (DateTimeField): Field for the date and time when the password entry was created.
        last_updated (DateTimeField): Field for the date and time when the password entry was last updated.

    Methods:
        cipher_suite: Property method returning the Fernet cipher suite instance used for encryption and decryption.
        encrypt_password(password): Method to encrypt the password using the Fernet cipher suite.
        decrypt_password(): Method to decrypt the encrypted password using the Fernet cipher suite.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    username = models.CharField(max_length=255)
    encrypted_password = models.BinaryField()
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def cipher_suite(self):

        """
        Property method returning the Fernet cipher suite instance.

        This method returns the Fernet cipher suite instance initialized with the cryptographic key from the
        settings.CRYPTO_KEY.

        :return: Fernet cipher suite instance.
        """
        return Fernet(settings.CRYPTO_KEY)

    def encrypt_password(self, password):
        """
        Method to encrypt the password using the Fernet cipher suite.

        This method encrypts the provided password using the Fernet cipher suite instance and returns the
        encrypted password.

        :param password: The password to be encrypted.
        :return: The encrypted password.
        """
        return self.cipher_suite.encrypt(password)

    def decrypt_password(self):
        """
        Method to decrypt the encrypted password using the Fernet cipher suite.

        This method decrypts the encrypted password stored in the encrypted_password field using the Fernet
        cipher suite instance and returns the decrypted password.

        :return: The decrypted password, or None if decryption fails.
        """
        try:
            decrypted_password = self.cipher_suite.decrypt(self.encrypted_password).decode('utf-8')
            return decrypted_password
        except InvalidToken:
            logger.error(f'Trying to decrypt password: Invalid decryption token!')
            return None
