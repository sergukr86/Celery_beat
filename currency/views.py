import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Max

from .models import Rate
from .forms import CalculatorForm


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


def calculator(request):
    if request.method == "GET":
        form = CalculatorForm()
        return render(request, "calculator.html", {"form": form})
    form = CalculatorForm(request.POST)
    if form.is_valid():
        currency_from = form.cleaned_data["currency_from"]
        currency_to = form.cleaned_data["currency_to"]
        amount = form.cleaned_data["amount"]
        date = datetime.date.today()
        # filter by date and currency
        provider = Rate.objects.filter(
            cur_from=currency_from, cur_to=currency_to, date=date
        )
        # filter by max rate
        max_rate = provider.aggregate(max_sell=Max("sell"))["max_sell"]
        # calculate answer
        answer = amount * max_rate
        return render(request, "calculator.html", {"answer": answer})
    return render(request, "calculator.html")
