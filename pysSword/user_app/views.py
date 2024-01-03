from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileUpdateForm, EmailUserCreationForm, EmailAuthenticationForm


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

    return render(request, 'auth_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user, backend='user_app.backends.EmailAuthBackend')
                messages.success(request, f'Welcome, {email}!')
                return redirect('profile')
            else:
                print('error')
                messages.error(request, 'Invalid username or password.')

    else:
        form = EmailAuthenticationForm()

    return render(request, 'auth_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


@login_required
def user_profile(request):
    if request.method == 'POST':
        # Обработка формы обновления профиля
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')

        # Обработка формы изменения пароля
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Обновляем сессию после изменения пароля
            messages.success(request, 'Your password was successfully updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating password. Please correct the errors.')
    else:
        profile_form = UserProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'auth_app/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
