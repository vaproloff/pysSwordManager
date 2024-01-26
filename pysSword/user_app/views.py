from allauth.account.decorators import reauthentication_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import *


@login_required
@reauthentication_required
def user_profile(request):
    # if request.method == 'POST':
    #     form_type = request.POST.get('form_type')
    #     match form_type:
    #         case 'first_name':
    #             form = EditFirstNameForm(request.POST, instance=request.user)
    #         case 'last_name':
    #             form = EditLastNameForm(request.POST, instance=request.user)
    #         case 'phone_number':
    #             form = EditPhoneNumberForm(request.POST, instance=request.user)
    #         case 'password':
    #             form = PasswordChangeForm(request.user, request.POST)
    #         case _:
    #             form = None
    #
    #     if form is not None and form.is_valid():
    #         user = form.save()
    #         if form_type == 'password':
    #             update_session_auth_hash(request, user)  # Обновляем сессию после изменения пароля
    #         messages.success(request, 'Your profile has been updated successfully.')
    #         return redirect('profile')
    #     else:
    #         messages.error(request, 'Error updating profile. Please correct the errors.')

    return render(request, 'user_app/profile.html', {
        'password_form': PasswordChangeForm(request.user),
    })
