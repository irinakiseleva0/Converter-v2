from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
import requests


def welcome(request):
    """
    Landing page: welcome text + buttons:
    - Go to converter
    - Register (optional)
    """
    return render(request, 'exchange_app/welcome.html')


def exchange(request):
    # Получаем курсы
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        data = response.json()
        currencies = data.get('rates', {})
    except Exception:
        currencies = {}

    context = {
        'currencies': currencies
    }

    if request.method == 'POST':
        from_amount_raw = request.POST.get('from-amount')
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        context.update({
            'from_amount': from_amount_raw,
            'from_curr': from_curr,
            'to_curr': to_curr,
        })

        try:
            from_amount = float(from_amount_raw)

            if from_curr in currencies and to_curr in currencies:
                converted_amount = round(
                    (currencies[to_curr] / currencies[from_curr]) * from_amount,
                    2
                )
                context['converted_amount'] = converted_amount
            else:
                context['error'] = "Unknown currency code."
        except (TypeError, ValueError):
            context['error'] = "Invalid amount."

    return render(request, 'exchange_app/index.html', context)


def REG_FUNC(request):
    """Simple optional registration."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if not username or not password1 or not password2:
            messages.error(request, "Please fill all required fields.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            # сразу логиним пользователя
            auth_login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('converter')

    return render(request, 'exchange_app/index_reg.html')
