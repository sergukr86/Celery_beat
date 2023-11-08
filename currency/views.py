import datetime

from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import CalculatorForm
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
        max_rate = round(provider.aggregate(max_sell=Max("sell"))["max_sell"], 3)
        bank = provider.get(sell=max_rate)
        # calculate answer
        answer = float(amount) * float(max_rate)
        return render(request,"calculator.html",
                      {"answer": answer,
                       "form": form,
                       "amount": amount,
                       "max_rate": max_rate,
                       "currency_from": currency_from,
                       "currency_to": currency_to,
                       "bank": bank
        })
    return redirect("calculator")

