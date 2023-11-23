
from currency.provider import MonoProvider, PrivatbankProvider, NacbankProvider, VkurseProvider, SellBuy

from unittest.mock import MagicMock, patch


def test_mono_provider():
    provider = MonoProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27, buy=28))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27, buy=28)
    rate_mocked.assert_called()


def test_mono_with_data():
    provider = MonoProvider("USD", "UAH")
    with patch("currency.provider.requests.get") as mocked_get:
        mocked_get().json.return_value = [
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateBuy": 28.0,
                "rateSell": 27.0,
            }
        ]
        rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=28.0)
