from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileUpdateForm


@login_required
def user_profile(request):
    if request.method == 'POST':
        # Обработка формы обновления профиля
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors.')

        # Обработка формы изменения пароля
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Обновляем сессию после изменения пароля
            messages.success(request, 'Your password was successfully updated.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Error updating password. Please correct the errors.')
    else:
        profile_form = UserProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'user_profile/user_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
