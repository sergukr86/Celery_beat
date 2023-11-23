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
