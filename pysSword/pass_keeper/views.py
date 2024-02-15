import logging

from allauth.account.decorators import reauthentication_required
from allauth.account.reauthentication import record_authentication
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import PasswordEntry
from .forms import PasswordEntryForm
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('app')


@login_required
@reauthentication_required
def password_list(request):
    """
    View function to display a list of password entries.

    This function requires the user to be authenticated and reauthenticated if necessary before accessing the
    password list. It retrieves the password entries associated with the current user from the database and orders
    them by their titles. The list of password entries is then rendered using the 'pass_keeper/password_list.html'
    template.

    :param request: HttpRequest object representing the request made to the server.
    :return: HttpResponse object rendering the password list template with the password entries.

    """
    record_authentication(request, request.user)
    entries = PasswordEntry.objects.filter(user=request.user).order_by('title')
    return render(request, 'pass_keeper/password_list.html', {'entries': entries})


@login_required
def create_password(request):
    """
    View function to handle the creation of a new password entry.

    This function allows authenticated users to create new password entries. If the request method is POST,
    it processes the submitted form data, validates it, and saves the new password entry to the database.
    If the creation is successful, it displays a success message and logs the action. Then, it redirects the
    user to the password list page, highlighting the newly created entry. If there is any error during the
    creation process, it displays an error message and logs the error, redirecting the user back to the password
    list page.

    If the request method is not POST, but the 'Sec-Fetch-Mode' header is set to 'cors', it initializes an
    empty password entry form to be rendered for the user to fill in. Otherwise, it raises a Http404 exception.

    :param request: HttpRequest object representing the request made to the server.
    :return: HttpResponse object rendering the password entry form or redirecting to the password list page.

    """
    if request.method == 'POST':
        record_authentication(request, request.user)
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            messages.success(request, 'Новый пароль был создан успешно')
            logger.info(f'New password created successfully ({request.user.email})')
            return redirect(reverse('password_list') + f'#entry_{entry.id}')
        else:
            messages.error(request, 'Ошибка при создании пароля')
            logger.error(f'Error while creating new password ({request.user.email})')
            return redirect('password_list')

    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        record_authentication(request, request.user)
        form = PasswordEntryForm()
        return render(request, 'pass_keeper/create_password.html', {'form': form})
    else:
        raise Http404()


@login_required
def edit_password(request, entry_id):
    """
    View function to handle the editing of an existing password entry.

    This function allows authenticated users to edit an existing password entry identified by its entry_id.
    If the entry_id does not exist for the authenticated user, a 404 page not found error is raised.
    If the request method is POST, it processes the submitted form data, validates it, and saves the edited
    password entry to the database. If the edit is successful, it displays a success message and logs the action.
    Then, it redirects the user to the password list page, highlighting the edited entry. If there is any error
    during the editing process, it displays an error message and logs the error, redirecting the user back to
    the password list page.

    If the request method is not POST, but the 'Sec-Fetch-Mode' header is set to 'cors', it initializes a
    password entry form populated with the existing data of the password entry to be edited. It also checks
    whether the edited password would result in a duplicate entry. If so, it sets a flag to indicate duplicate
    status. Otherwise, it raises a Http404 exception.

    :param request: HttpRequest object representing the request made to the server.
    :param entry_id: Identifier of the password entry to be edited.
    :return: HttpResponse object rendering the password entry form or redirecting to the password list page.

    """
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    record_authentication(request, request.user)

    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=password_entry)
        if form.is_valid():
            form.save()

            logger.info(f'Password edited and saved successfully ({request.user.email})')
            messages.success(request, 'Пароль сохранён успешно')
        else:
            logger.error(f'Error while editing existing password ({request.user.email})')
            messages.error(request, 'Ошибка при изменении пароля')

        return redirect(reverse('password_list') + f'#entry_{entry_id}')

    elif request.headers.get('Sec-Fetch-Mode') == 'cors':
        form = PasswordEntryForm(instance=password_entry)

        else_entries = PasswordEntry.objects.filter(user=request.user).exclude(pk=password_entry.pk)
        is_duplicate = password_entry.decrypt_password() in [entry.decrypt_password() for entry in else_entries]

        return render(request, 'pass_keeper/edit_password.html',
                      {'form': form, 'password_entry': password_entry, 'is_duplicate': is_duplicate})
    else:
        raise Http404()


@login_required
def delete_password(request, entry_id):
    """
    View function to handle the deletion of a password entry.

    This function allows authenticated users to delete an existing password entry identified by its entry_id.
    If the entry_id does not exist for the authenticated user, a 404 page not found error is raised.
    The function deletes the password entry from the database and logs the action. It then displays a success
    message and redirects the user to the password list page.

    :param request: HttpRequest object representing the request made to the server.
    :param entry_id: Identifier of the password entry to be deleted.
    :return: HttpResponse object redirecting to the password list page.

    """
    password_entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    password_entry.delete()

    record_authentication(request, request.user)
    logger.info(f'Password deleted successfully ({request.user.email})')
    messages.success(request, 'Пароль успешно удалён')
    return redirect('password_list')
