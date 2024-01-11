from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import *


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('login')
    else:
        form = EmailUserCreationForm()

    return render(request, 'user_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user, backend='user_app.backends.EmailAuthBackend')
                messages.success(request, f'Welcome, {email}!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = EmailAuthenticationForm()

    return render(request, 'user_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        match form_type:
            case 'first_name':
                form = EditFirstNameForm(request.POST, instance=request.user)
            case 'last_name':
                form = EditLastNameForm(request.POST, instance=request.user)
            case 'phone_number':
                form = EditPhoneNumberForm(request.POST, instance=request.user)
            case 'password':
                form = PasswordChangeForm(request.user, request.POST)
            case _:
                form = None

        if form is not None and form.is_valid():
            user = form.save()
            if form_type == 'password':
                update_session_auth_hash(request, user)  # Обновляем сессию после изменения пароля
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')

    return render(request, 'user_app/profile.html', {
        'password_form': PasswordChangeForm(request.user),
    })


class CustomPasswordResetView(PasswordResetView):
    template_name = 'user_app/password_reset_form.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user_app/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_app/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user_app/password_reset_complete.html'
