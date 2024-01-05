from django.shortcuts import render, get_object_or_404, redirect
from .models import PasswordEntry
from .forms import PasswordEntryForm, PasswordEntrySearchForm, PasswordEditEntryForm
from django.contrib.auth.decorators import login_required


@login_required
def password_list(request):
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
    pass_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    decrypted_password = pass_entry.decrypt_password()
    return render(request, 'pass_keeper/password_detail.html',
                  {'password': pass_entry, 'decrypted_password': decrypted_password})


@login_required
def create_password(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('password_list')
    else:
        form = PasswordEntryForm()

    return render(request, 'pass_keeper/create_password.html', {'form': form})


@login_required
def edit_password(request, entry_id):
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = PasswordEditEntryForm(request.POST, instance=password_entry)
        if form.is_valid():
            form.save()
            return redirect('password_detail', entry_id=password_entry.id)
    else:
        decrypted_password = password_entry.decrypt_password()
        initial_data = {
            'title': password_entry.title,
            'website': password_entry.website,
            'username': password_entry.username,
            'password': decrypted_password,
            'notes': password_entry.notes,
        }
        form = PasswordEditEntryForm(instance=password_entry, initial=initial_data)

    return render(request, 'pass_keeper/edit_password.html',
                  {'form': form, 'password_entry': password_entry})


@login_required
def delete_password(request, entry_id):
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    password_entry.delete()
    return redirect('password_list')
