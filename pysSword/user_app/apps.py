import logging

from allauth.account.signals import (
    user_logged_in,
    user_signed_up,
    password_changed,
    password_reset,
    email_confirmed,
    email_confirmation_sent,
)
from django.apps import AppConfig
from django.contrib.auth import user_logged_out
from django.dispatch import receiver

logger = logging.getLogger('app')


class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'


@receiver(user_logged_in)
def log_user_logged_in(request, user, **kwargs):
    logger.info(f'User {user.email} logged in successfully')


@receiver(user_logged_out)
def log_user_logged_out(request, user, **kwargs):
    logger.info(f'User {user.email} logged out')


@receiver(user_signed_up)
def log_user_signed_up(request, user, **kwargs):
    logger.info(f'User {user.email} signed up successfully')


@receiver(password_changed)
def log_password_changed(request, user, **kwargs):
    logger.info(f'User {user.email}\'s password changed successfully')


@receiver(password_reset)
def log_password_reset(request, user, **kwargs):
    logger.info(f'User {user.email}\'s password reset successfully')


@receiver(email_confirmed)
def log_email_confirmed(request, email_address, **kwargs):
    logger.info(f'User\'s email {email_address} confirmed successfully')


@receiver(email_confirmation_sent)
def log_email_confirmation_sent(request, confirmation, signup, **kwargs):
    logger.info(f'User {confirmation.email_address}\'s confirmation email sent successfully')
