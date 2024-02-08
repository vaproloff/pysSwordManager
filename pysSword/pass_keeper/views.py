import logging

from allauth.account.decorators import reauthentication_required
from allauth.account.reauthentication import record_authentication
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import PasswordEntry
from .forms import PasswordEntryForm
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('app')


@login_required
@reauthentication_required
def password_list(request):
    record_authentication(request, request.user)
    entries = PasswordEntry.objects.filter(user=request.user).order_by('title')
    return render(request, 'pass_keeper/password_list.html', {'entries': entries})


@login_required
def create_password(request):
    if request.method == 'POST':
        record_authentication(request, request.user)
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            logger.info(f'New password created successfully ({request.user.email})')
            messages.success(request, 'Новый пароль был создан успешно')
            return redirect('password_list')

        logger.error(f'Error while creating new password ({request.user.email})')
    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        record_authentication(request, request.user)
        form = PasswordEntryForm()
        return render(request, 'pass_keeper/create_password.html', {'form': form})
    else:
        raise Http404()


@login_required
def edit_password(request, entry_id):
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    record_authentication(request, request.user)

    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=password_entry)
        if form.is_valid():
            form.save()

            logger.info(f'Password edited and saved successfully ({request.user.email})')
            messages.success(request, 'Пароль сохранён успешно')
            return redirect('password_list')

        logger.error(f'Error while editing existing password ({request.user.email})')
    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        form = PasswordEntryForm(instance=password_entry)
        return render(request, 'pass_keeper/edit_password.html',
                      {'form': form, 'password_entry': password_entry})
    else:
        raise Http404()


@login_required
def delete_password(request, entry_id):
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    password_entry.delete()

    record_authentication(request, request.user)
    logger.info(f'Password deleted successfully ({request.user.email})')
    messages.success(request, 'Пароль удалён')
    return redirect('password_list')
