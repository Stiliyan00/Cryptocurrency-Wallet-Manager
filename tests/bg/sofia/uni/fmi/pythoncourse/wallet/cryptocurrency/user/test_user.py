from unittest import mock

import pytest

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.repository.CryptocurrencyCoinsAPIClient import \
    CryptocurrencyCoinsAPIClient
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.StandardUser import StandardUser
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.CryptocurrencyDoesNotExistException import \
    CryptocurrencyDoesNotExistException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.NotEnoughMoneyError import \
    NotEnoughMoneyError
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.UserDoesNotHaveCryptocurrencyException import \
    UserDoesNotHaveCryptocurrencyException


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://rest.coinapi.io/v1/exchangerate/BTC/USD':
        return MockResponse({"asset_id": "BTC", "rate": 21676.00}, 200)
    elif args[0] == 'https://rest.coinapi.io/v1/exchangerate/NIS/USD':
        return MockResponse({"asset_id": "NIS", "rate": 0.28}, 200)
    elif args[0] == 'https://rest.coinapi.io/v1/exchangerate/LTC/USD':
        return MockResponse({"asset_id": "LTC", "rate": 93.92}, 200)

    return MockResponse(None, 404)


@pytest.mark.parametrize("invalid_deposit_amount", [
    0,
    -1000
])
def test_deposit_with_invalid_amount_of_money_should_raise_exception(invalid_deposit_amount):
    user = StandardUser(username='stiliyan', password='password1', assets={})
    with pytest.raises(ValueError):
        user.deposit_money(invalid_deposit_amount)


def test_initial_deposit_money_positive_amount_of_money():
    user = StandardUser(username='stiliyan', password='password1', assets={})

    money_to_be_deposit: float = 10000
    # Deposit the money in the user account
    user.deposit_money(money_to_be_deposit)
    assert user.get_money() == money_to_be_deposit


def test_deposit_after_several_successful_deposit_actions():
    user = StandardUser(username='stiliyan', password='password1', assets={})

    money_to_be_deposit: float = 0

    # Initial deposit the money in the user account
    user.deposit_money(9899)
    # Add the deposit money to money_to_be_deposit:
    money_to_be_deposit += 9899

    # Second time to deposit a positive amount of money
    user.deposit_money(1000)
    # Add the deposit money to money_to_be_deposit:
    money_to_be_deposit += 1000

    # Third time to deposit a positive amount of money
    user.deposit_money(10000)
    # Add the deposit money to money_to_be_deposit:
    money_to_be_deposit += 10000
    # Assert that the deposit money is as expected:
    assert user.get_money() == money_to_be_deposit


@pytest.mark.parametrize("buy_invalid_cryptocurrency_amount", [
    0,
    -1000
])
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_buy_with_invalid_amount_of_cryptocurrency_should_raise_exception(mock_get, buy_invalid_cryptocurrency_amount):
    user = StandardUser(username='stiliyan', password='password1', assets={})
    existing_offering_code = 'BTC'
    # Test:
    with pytest.raises(ValueError):
        user.buy(existing_offering_code, buy_invalid_cryptocurrency_amount)


@pytest.mark.parametrize("existing_cryptocurrency_offering_code", [
    'BTC',
    'NIS',
    'LTC'
])
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_buy_any_cryptocurrency_with_no_money_should_raise_exception(mock_get, existing_cryptocurrency_offering_code):
    user = StandardUser(username='stiliyan', password='password1', assets={})

    # Test:
    with pytest.raises(NotEnoughMoneyError):
        user.buy(existing_cryptocurrency_offering_code, 0.001)


@pytest.mark.parametrize("existing_cryptocurrency_offering_code", [
    'BTC',
    'NIS',
    'LTC'
])
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_buy_with_not_enough_money_should_raise_exception(mock_get, existing_cryptocurrency_offering_code):
    user = StandardUser(username='stiliyan', password='password1', assets={})

    # Get the rate of the existing cryptocurrency:
    cryptocurrency_rate = \
        CryptocurrencyCoinsAPIClient.get_specific_rate_of_currency(
            existing_cryptocurrency_offering_code,
            'USD').json()['rate']

    # Deposit not enough money to buy the amount of cryptocurrency:
    user.deposit_money(cryptocurrency_rate - (cryptocurrency_rate * 0.1))
    # Test:
    with pytest.raises(NotEnoughMoneyError):
        user.buy(existing_cryptocurrency_offering_code, 1)


@pytest.mark.parametrize("none_existing_cryptocurrency_offering_code", [
    'random_non_exiting_offering_code',
    'NISs',
    ''
])
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_buy_with_non_existing_cryptocurrency_offering_code_should_raise_exception(
        mock_exists,
        none_existing_cryptocurrency_offering_code):
    user = StandardUser(username='stiliyan', password='password1', assets={})
    with pytest.raises(CryptocurrencyDoesNotExistException):
        user.buy(none_existing_cryptocurrency_offering_code, 1)


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_buy_with_initial_buying_of_existing_cryptocurrency_offering_code(mock_get):
    user = StandardUser(username='stiliyan', password='password1', assets={})

    existing_offering_code = 'BTC'

    # Get the rate of the existing cryptocurrency:
    cryptocurrency_rate = \
        CryptocurrencyCoinsAPIClient.get_specific_currency_data(existing_offering_code).json()['rate']

    # Deposit enough money to buy the amount of a cryptocurrency:
    money_to_be_deposit = cryptocurrency_rate * 2
    user.deposit_money(money_to_be_deposit)

    # Buy the cryptocurrency:
    user.buy(existing_offering_code, 1)

    # Test:
    # Assert the money:
    assert user.get_money() == money_to_be_deposit - cryptocurrency_rate
    # Assert that the asset is added:
    assert user.get_assets().get(existing_offering_code) is not None
    print(user.get_assets().get('non_existing_offering_code'))


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_buy_with_second_time_buying_of_existing_cryptocurrency_offering_code(mock_get):
    user = StandardUser(username='stiliyan', password='password1', assets={})

    existing_offering_code = 'BTC'

    # Get the rate of the existing cryptocurrency:
    cryptocurrency_rate = \
        CryptocurrencyCoinsAPIClient.get_specific_currency_data(existing_offering_code).json()['rate']

    # Deposit enough money to buy the amount of a cryptocurrency:
    money_to_be_deposit = cryptocurrency_rate * 4
    user.deposit_money(money_to_be_deposit)

    # Buy the cryptocurrency for the first time:
    user.buy(existing_offering_code, 1)
    # Buy the cryptocurrency for the second time:
    user.buy(existing_offering_code, 1)

    # Test:
    # Assert the money:
    assert user.get_money() == money_to_be_deposit - (cryptocurrency_rate * 2)
    # Assert that the asset is added:
    assert user.get_assets().get(existing_offering_code) is not None
    print(user.get_assets().get('non_existing_offering_code'))


@mock.patch('requests.get', side_effect=mocked_requests_get)
@pytest.mark.parametrize("offering_code", [
    'BTC',
    'non_existing_offering_code'
])
def test_sell_with_invalid_cryptocurrency_offering_code_should_raise_exception(mock_get, offering_code):
    user = StandardUser(username='stiliyan', password='password1', assets={})
    # Test:
    with pytest.raises(UserDoesNotHaveCryptocurrencyException):
        user.sell(offering_code=offering_code)


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_sell_with_exiting_offering_code(mock_get):
    user = StandardUser(username='stiliyan', password='password1', assets={'BTC': 1.2})
    # Store the cryptocurrency value:
    cryptocurrency_value = CryptocurrencyCoinsAPIClient.get_specific_currency_data('BTC').json()['rate'] * 1.2
    # Sell this cryptocurrency:
    assert cryptocurrency_value == user.sell('BTC')
    # Assert that the money is added:
    assert user.get_money() == cryptocurrency_value
    # Assert that the asset is no longer in the user account:
    assert user.get_assets().get('BTC') is None
