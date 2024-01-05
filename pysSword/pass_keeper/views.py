from django.shortcuts import render, get_object_or_404, redirect
from .models import PasswordEntry
from .forms import PasswordEntryForm, PasswordEntrySearchForm
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
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    return render(request, 'pass_keeper/password_detail.html', {'entry': entry})


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
