import logging

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
        form = PasswordGeneratorForm(request.POST)
        if form.is_valid():
            pass_quantity = form.cleaned_data['pass_quantity']
            pass_length = form.cleaned_data['pass_length']
            include_digits = form.cleaned_data['include_digits']
            include_lowercase = form.cleaned_data['include_lowercase']
            include_uppercase = form.cleaned_data['include_uppercase']
            include_symbols = form.cleaned_data['include_symbols']
            custom_symbols = form.cleaned_data['custom_symbols']

            if request.user.is_authenticated:
                if settings:
                    settings.pass_quantity = pass_quantity
                    settings.pass_length = pass_length
                    settings.include_digits = include_digits
                    settings.include_lowercase = include_lowercase
                    settings.include_uppercase = include_uppercase
                    settings.include_symbols = include_symbols
                    settings.custom_symbols = custom_symbols
                    settings.save()
                else:
                    PasswordGenerationSettings.objects.create(
                        user=request.user, pass_quantity=pass_quantity, pass_length=pass_length,
                        include_digits=include_digits, include_lowercase=include_lowercase,
                        include_uppercase=include_uppercase, include_symbols=include_symbols,
                        custom_symbols=custom_symbols
                    )

                logger.info(f'Password generator setting saved successfully ({request.user.email})')

            generated_passwords = generate_passwords(
                pass_quantity, pass_length, include_digits,
                include_lowercase, include_uppercase, include_symbols, custom_symbols
            )
            return render(request, 'pass_gen/generator.html',
                          {'form': form, 'passwords': generated_passwords,
                           'settings_saved': True if request.user.is_authenticated else False})
    else:
        form_data = {}
        if settings:
            form_data = {
                'pass_quantity': settings.pass_quantity,
                'pass_length': settings.pass_length,
                'include_digits': settings.include_digits,
                'include_lowercase': settings.include_lowercase,
                'include_uppercase': settings.include_uppercase,
                'include_symbols': settings.include_symbols,
                'custom_symbols': settings.custom_symbols,
            }
        form = PasswordGeneratorForm(initial=form_data)

    return render(request, 'pass_gen/generator.html', {'form': form, 'passwords': None, 'settings_saved': False})


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
