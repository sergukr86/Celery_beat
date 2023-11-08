import datetime

from celery import shared_task
from currency.provider import PROVIDERS
from currency.models import Rate


@shared_task
def pull_rate():
    date = datetime.date.today()
    for provider_class in PROVIDERS:
        provider_eur = provider_class("EUR", "UAH")

        print("EUR", provider_eur.name)

        eur = Rate.objects.filter(
            vendor=provider_eur.name, cur_from="EUR", cur_to="UAH", date=date
        )
        if not eur.exists():
            euro_rate = provider_eur.get_rate()
            eur = Rate.objects.create(
                vendor=provider_eur.name,
                cur_from="EUR",
                cur_to="UAH",
                buy=euro_rate.buy,
                sell=euro_rate.sell,
                date=date,
            )
            print(eur)

        provider_usd = provider_class("USD", "UAH")
        print("USD", provider_usd.name)

        usd = Rate.objects.filter(
            vendor=provider_usd.name,
            cur_from="USD",
            cur_to="UAH",
            date=date,
        )
        if not usd.exists():
            usd_rate = provider_usd.get_rate()
            usd = Rate.objects.create(
                vendor=provider_usd.name,
                cur_from="USD",
                cur_to="UAH",
                buy=usd_rate.buy,
                sell=usd_rate.sell,
                date=date,
            )
            print(usd.vendor)
