from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests


@api_view(['GET'])
def convert_api(request):
    """
    GET /api/convert/?from=USD&to=EUR&amount=100

    Returns JSON: {"from": "USD", "to": "EUR", "amount": 100.0, "result": 90.0}
    """
    from_curr = request.GET.get('from', '').upper()
    to_curr = request.GET.get('to', '').upper()
    amount_raw = request.GET.get('amount')

    if not from_curr or not to_curr or amount_raw is None:
        return Response(
            {"error": "Missing required parameters: from, to, amount."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        amount = float(amount_raw)
    except (TypeError, ValueError):
        return Response(
            {"error": "Amount must be a valid number."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if amount <= 0:
        return Response(
            {"error": "Amount must be greater than zero."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if amount > 1_000_000_000:
        return Response(
            {"error": "Amount is too large."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        response.raise_for_status()
        rates = response.json().get('rates', {})
    except Exception:
        return Response(
            {"error": "Currency service is temporarily unavailable."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    if from_curr not in rates or to_curr not in rates:
        return Response(
            {"error": "Unknown currency code."},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = round((rates[to_curr] / rates[from_curr]) * amount, 2)

    return Response({
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "result": result,
    })
