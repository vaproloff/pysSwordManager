from django.core.mail import EmailMessage
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
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from .forms import *
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, f'Account created for {user.email}!')
            messages.info(request, f'Please confirm your email address to complete the registration')
            mail_subject = 'Confirm your email to use Pyssword Manager.'
            message = render_to_string('user_app/activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.send()
            return redirect('login')
    else:
        form = EmailUserCreationForm()

    return render(request, 'user_app/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been confirmed! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user and user.is_active:
                login(request, user, backend='user_app.backends.EmailAuthBackend')
                messages.success(request, f'Welcome, {email}!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password or user is not active.')

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
