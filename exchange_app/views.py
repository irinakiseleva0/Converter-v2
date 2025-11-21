from django.shortcuts import render
import requests


def exchange(request):
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
    return render(request, 'exchange_app/index_reg.html')
