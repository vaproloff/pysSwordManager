from django.shortcuts import render
from .forms import PasswordGeneratorForm
from utils.pass_generator import generate_passwords


def password_generator(request):
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

            generated_passwords = generate_passwords(
                pass_quantity, pass_length, include_digits,
                include_lowercase, include_uppercase, include_symbols, custom_symbols
            )

            return render(request, 'pass_gen/generator.html',
                          {'form': form, 'passwords': generated_passwords})
    else:
        form = PasswordGeneratorForm()

    return render(request, 'pass_gen/generator.html', {'form': form, 'passwords': None})
