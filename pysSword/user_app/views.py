import logging

from allauth.account.reauthentication import record_authentication
from allauth.mfa import app_settings
from allauth.account.decorators import reauthentication_required
from allauth.account.forms import ChangePasswordForm
from allauth.mfa.models import Authenticator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import *

logger = logging.getLogger('app')


@login_required
@reauthentication_required
def user_profile(request):
    """
    View function to handle the user profile page.

    This function allows authenticated users to view and edit their profile information. It requires the user to be
    reauthenticated if necessary before accessing the profile page. The user can update their first name, last name,
    or password. Upon submission of the form, the function validates the data and saves the changes to the user's
    profile. If the form submission is successful, it displays a success message and logs the action. If there are
    any errors during the process, it displays an error message and logs the error.

    :param request: HttpRequest object representing the request made to the server.
    :return: HttpResponse object rendering the user profile page with relevant forms and data.
    """
    record_authentication(request, request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        match form_type:
            case 'first_name':
                form = EditFirstNameForm(request.POST, instance=request.user)
            case 'last_name':
                form = EditLastNameForm(request.POST, instance=request.user)
            case 'password':
                form = ChangePasswordForm(request.user, request.POST)
            case _:
                form = None

        if form is not None and form.is_valid():
            form.save()
            if form_type == 'password':
                update_session_auth_hash(request, request.user)

            logger.info(f'Successfully updated profile ({request.user.email})')
            messages.success(request, 'Профиль был обновлён успешно')
        else:
            logger.error(f'Error updating user profile ({request.user.email})')
            messages.error(request, 'Ошибка при обновлении данных профиля. Исправьте ошибки и попробуйте снова')

        return redirect('profile')

    return render(request, 'user_app/profile.html', {
        'password_form': ChangePasswordForm(request.user),
        'authenticators':
            {
                auth.type: auth.wrap()
                for auth in Authenticator.objects.filter(user=request.user)
            },
        'MFA_SUPPORTED_TYPES': app_settings.SUPPORTED_TYPES,
    })
