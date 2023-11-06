from django.http import JsonResponse
from .models import Rate


def main(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "date": rate.date,
                "vendor": rate.vendor,
                "currency_a": rate.cur_from,
                "currency_b": rate.cur_to,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }

    return JsonResponse(response_data)
