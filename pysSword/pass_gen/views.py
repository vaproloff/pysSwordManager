import logging

from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import PasswordGeneratorForm
from utils.pass_generator import generate_passwords
from .models import PasswordGenerationSettings

logger = logging.getLogger('app')


def password_generator(request):
    settings = None
    if request.user.is_authenticated:
        try:
            settings = PasswordGenerationSettings.objects.get(user=request.user)
        except PasswordGenerationSettings.DoesNotExist:
            pass

    if request.method == 'POST':
        form = PasswordGeneratorForm(request.POST, instance=settings)
        if form.is_valid():
            if request.user.is_authenticated:
                form.save()
                logger.info(f'Password generator setting saved successfully ({request.user.email})')
                messages.success(request, 'Настройки генератора паролей сохранены успешно!')

            generated_passwords = generate_passwords(**{field: form.cleaned_data[field] for field in form.cleaned_data})
            return render(request, 'pass_gen/generator.html', {'form': form, 'passwords': generated_passwords})
    else:
        form = PasswordGeneratorForm(initial=settings.__dict__ if settings else None)

    return render(request, 'pass_gen/generator.html', {'form': form, 'passwords': None})


@login_required
def pass_gen_api(request):
    try:
        settings = PasswordGenerationSettings.objects.get(user=request.user)
    except PasswordGenerationSettings.DoesNotExist:
        settings = None

    if settings:
        generated_password = generate_passwords(
            1, settings.pass_length, settings.include_digits,
            settings.include_lowercase, settings.include_uppercase, settings.include_symbols, settings.custom_symbols
        ).pop()
    else:
        generated_password = generate_passwords(pass_quantity=1).pop()

    return JsonResponse({'password': generated_password})
