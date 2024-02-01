import logging

from allauth.account.decorators import reauthentication_required
from allauth.account.reauthentication import record_authentication
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import PasswordEntry
from .forms import PasswordEntryForm, PasswordEntrySearchForm
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('app')


@login_required
@reauthentication_required
def password_list(request):
    record_authentication(request, request.user)

    entries = PasswordEntry.objects.filter(user=request.user)
    search_form = PasswordEntrySearchForm(request.GET)

    if search_form.is_valid():
        search_term = search_form.cleaned_data.get('search_term')
        if search_term:
            entries = entries.filter(title__icontains=search_term) | \
                      entries.filter(username__icontains=search_term) | \
                      entries.filter(notes__icontains=search_term) | \
                      entries.filter(website__icontains=search_term)

    return render(request, 'pass_keeper/password_list.html', {'entries': entries, 'search_form': search_form})


@login_required
def password_detail(request, entry_id):
    record_authentication(request, request.user)
    pass_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    if pass_entry.user != request.user:
        logger.error(f'Trying to access non-user password ({request.user.email})')
        return HttpResponseForbidden()
    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        return render(request, 'pass_keeper/password_detail.html',
                      {'password': pass_entry})


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
            return redirect('password_list')

        logger.error(f'Error while creating new password ({request.user.email})')
    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        record_authentication(request, request.user)
        form = PasswordEntryForm()
        return render(request, 'pass_keeper/create_password.html', {'form': form})
    else:
        return HttpResponseForbidden()


@login_required
def edit_password(request, entry_id):
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    if password_entry.user != request.user:
        logger.error(f'Trying to access non-user password ({request.user.email})')
        return HttpResponseForbidden()

    if request.method == 'POST':
        record_authentication(request, request.user)
        form = PasswordEntryForm(request.POST, instance=password_entry)
        if form.is_valid():
            form.save()

            logger.info(f'Password edited and saved successfully ({request.user.email})')
            return redirect('password_list')

        logger.error(f'Error while editing existing password ({request.user.email})')
    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        record_authentication(request, request.user)
        decrypted_password = password_entry.decrypt_password()
        initial_data = {
            'title': password_entry.title,
            'website': password_entry.website,
            'username': password_entry.username,
            'password': decrypted_password,
            'notes': password_entry.notes,
        }
        form = PasswordEntryForm(instance=password_entry, initial=initial_data)

        return render(request, 'pass_keeper/edit_password.html',
                      {'form': form, 'password_entry': password_entry})
    else:
        return HttpResponseForbidden()


@login_required
def delete_password(request, entry_id):
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    if password_entry.user != request.user:
        logger.error(f'Trying to access non-user password ({request.user.email})')
        return HttpResponseForbidden()

    record_authentication(request, request.user)
    password_entry.delete()

    logger.info(f'Password deleted successfully ({request.user.email})')
    return redirect('password_list')


@login_required
def get_password(request, entry_id):
    pass_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    if pass_entry.user != request.user:
        logger.error(f'Trying to access non-user password ({request.user.email})')
        return HttpResponseForbidden()

    if request.headers.get('Sec-Fetch-Mode') == 'cors':
        record_authentication(request, request.user)
        return JsonResponse({'password': pass_entry.decrypt_password()})
    else:
        return HttpResponseForbidden()
