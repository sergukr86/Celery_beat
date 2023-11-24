import dataclasses

import requests
from abc import ABC, abstractmethod


class ProviderBase(ABC):
    name = None

    def __init__(self, curr_from, curr_to):
        self.curr_from = curr_from
        self.curr_to = curr_to

    @abstractmethod
    def get_rate(self):
        raise NotImplementedError("get_rate not implemented")


@dataclasses.dataclass
class SellBuy:
    sell: float
    buy: float


class MonoProvider(ProviderBase):
    name = "monobank"
    iso_from_country_code = {
        "UAH": 980,
        "EUR": 978,
        "USD": 840,
    }

    def get_rate(self) -> SellBuy:
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()
        curr_from_code = self.iso_from_country_code[self.curr_from]
        curr_to_code = self.iso_from_country_code[self.curr_to]

        for currency in response.json():
            if (
                currency["currencyCodeA"] == curr_from_code
                and currency["currencyCodeB"] == curr_to_code
            ):
                result = SellBuy(
                    sell=float(currency["rateSell"]), buy=float(currency["rateBuy"])
                )
                return result


class PrivatbankProvider(ProviderBase):
    name = "privatbank"

    def get_rate(self) -> SellBuy:
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
        response = requests.get(url)
        response.raise_for_status()
        curr_from_code = self.curr_from
        curr_to_code = self.curr_to

        for currency in response.json():
            if (
                currency["ccy"] == curr_from_code
                and currency["base_ccy"] == curr_to_code
            ):
                value = SellBuy(
                    sell=float(currency["buy"]), buy=float(currency["sale"])
                )
                return value


class NacbankProvider(ProviderBase):
    name = "nbu"

    def get_rate(self) -> SellBuy:
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        response = requests.get(url)
        response.raise_for_status()
        curr_from_code = self.curr_from
        for currency in response.json():
            if currency["cc"] == curr_from_code:
                value = SellBuy(
                    sell=float(currency["rate"]), buy=float(currency["rate"])
                )
                return value


class VkurseProvider(ProviderBase):
    name = "vkurse"
    from_country_code = {
        "EUR": "Euro",
        "USD": "Dollar",
    }

    def get_rate(self):
        url = "https://vkurse.dp.ua/course.json"
        response = requests.get(url)
        response.raise_for_status()
        curr_from_code = self.from_country_code[self.curr_from]
        cources = response.json()[0]
        buy_rate = cources[curr_from_code]["buy"]
        sell_rate = cources[curr_from_code]["sale"]
        value = SellBuy(buy=float(buy_rate), sell=float(sell_rate))
        return value


PROVIDERS = [MonoProvider, PrivatbankProvider, NacbankProvider, VkurseProvider]
