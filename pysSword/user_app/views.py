from allauth.account.decorators import reauthentication_required
from allauth.account.forms import ChangePasswordForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import *


@login_required
@reauthentication_required
def user_profile(request):
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
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')

    return render(request, 'user_app/profile.html', {
        'password_form': ChangePasswordForm(request.user),
    })
