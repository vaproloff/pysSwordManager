import logging

from django.contrib.auth.models import User
from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

logger = logging.getLogger('app')


class PasswordEntry(models.Model):
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
        return Fernet(settings.CRYPTO_KEY)

    def encrypt_password(self, password):
        return self.cipher_suite.encrypt(password)

    def decrypt_password(self):
        try:
            decrypted_password = self.cipher_suite.decrypt(self.encrypted_password).decode('utf-8')
            return decrypted_password
        except InvalidToken:
            logger.error(f'Trying to decrypt password: Invalid decryption token!')
            return None
