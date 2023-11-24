import responses

from currency.provider import (
    MonoProvider,
    PrivatbankProvider,
    NacbankProvider,
    VkurseProvider,
    SellBuy,
)

from unittest.mock import MagicMock


def test_mono_provider():
    provider = MonoProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27, buy=28))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27, buy=28)
    rate_mocked.assert_called()


@responses.activate
def test_mono_with_data():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=[
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateBuy": 38.0,
                "rateSell": 37.0,
            }
        ],
    )
    provider = MonoProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=37.0, buy=38.0)


def test_privat_provider():
    provider = PrivatbankProvider("EUR", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=40.0, buy=40.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=40.0, buy=40.5)
    rate_mocked.assert_called()


@responses.activate
def test_privat_with_data():
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        json=[
            {
                "ccy": "USD",
                "base_ccy": "UAH",
                "buy": 38.0,
                "sale": 37.0,
            }
        ],
    )
    provider = PrivatbankProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=38.0, buy=37.0)


def test_nbu_provider():
    provider = NacbankProvider("EUR", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=40.0, buy=40.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=40.0, buy=40.5)
    rate_mocked.assert_called()


@responses.activate
def test_nbu_with_data():
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=[
            {
                "cc": "USD",
                "rate": 38.0,
            }
        ],
    )
    provider = NacbankProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=38.0, buy=38.0)


def test_vkurse_provider():
    provider = VkurseProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=37.0, buy=37.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=37.0, buy=37.5)
    rate_mocked.assert_called()


@responses.activate
def test_vkurse_with_data():
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=[
            {
                "Dollar": {
                    "buy": 38.0,
                    "sale": 37.0
                }
            }
        ],
    )
    provider = VkurseProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=37.0, buy=38.0)
