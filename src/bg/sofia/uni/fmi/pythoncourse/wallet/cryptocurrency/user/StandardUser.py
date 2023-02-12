import json
from json import JSONEncoder

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.repository.CryptocurrencyCoinsAPIClient import \
    CryptocurrencyCoinsAPIClient
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.CryptocurrencyDoesNotExistException import \
    CryptocurrencyDoesNotExistException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.NotEnoughMoneyError import \
    NotEnoughMoneyError
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.UserDoesNotHaveCryptocurrencyException import \
    UserDoesNotHaveCryptocurrencyException


class StandardUser(User):
    RESPONSE_STATUS_CODE_OK = 200

    def __init__(self, username: str, password: str, assets: dict, money=0):
        self.__username = username
        self.__password = password
        self.__money = money
        self.__assets = assets

    def __cryptocurrency_exists(self, offering_code) -> bool:
        self.__validate_offering_code(offering_code)
        return CryptocurrencyCoinsAPIClient.get_specific_currency_data(offering_code).status_code == \
               self.RESPONSE_STATUS_CODE_OK

    def __validate_offering_code(self, offering_code: str):
        if offering_code is None:
            raise ValueError('Offering code cannot be None!')

    def __get_value_of_cryptocurrency_by_amount(self, offering_code: str, amount: float) -> float:
        return amount * CryptocurrencyCoinsAPIClient.get_specific_currency_data(offering_code).json()['rate']

    def __get_money_for_amount_of_cryptocurrency(self, offering_code: str):
        return CryptocurrencyCoinsAPIClient.get_specific_currency_data(offering_code).json()['rate'] * \
               self.__assets[offering_code]

    def deposit_money(self, amount: float):
        if amount <= 0.0:
            raise ValueError('Invalid amount for deposit! You cannot deposit 0 or less dollars!')
        self.__money += amount

    def buy(self, offering_code: str, amount: float):
        self.__validate_offering_code(offering_code)
        # The amount is the money not the asset
        if amount <= 0.0:
            raise ValueError('The wanted cryptocurrency ' + offering_code + ' cannot be 0.0 or less!')
        if not self.__cryptocurrency_exists(offering_code):
            raise CryptocurrencyDoesNotExistException(offering_code)

        value = self.__get_value_of_cryptocurrency_by_amount(offering_code, amount)
        if value > self.__money:
            raise NotEnoughMoneyError(amount)
        self.__money -= value

        if offering_code in self.__assets:
            self.__assets[offering_code] += amount
        else:
            self.__assets[offering_code] = amount

    def sell(self, offering_code: str) -> float:
        self.__validate_offering_code(offering_code)
        if offering_code not in self.__assets:
            raise UserDoesNotHaveCryptocurrencyException(offering_code)
        value: float = self.__get_money_for_amount_of_cryptocurrency(offering_code)
        self.__money += value
        self.__assets.pop(offering_code)  # Removing the asset from the list
        return value

    def is_valid_password(self, password: str) -> bool:
        return password == self.__password

    def get_username(self) -> str:
        return self.__username

    def get_money(self) -> float:
        return self.__money

    def get_assets(self) -> dict:
        return self.__assets.copy()

    def __iter__(self):
        for key in self.__dict__:
            yield key[len('_StandardUser__'):], getattr(self, key)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, StandardUser):
            return self.__username == other.__username and self.__password == other.__password and \
                   self.__money == other.__money and self.__assets.__eq__(other.__assets)
        return False

    def __hash__(self):
        # The hashing will user the username because it should be unique:
        return hash(self.__username)


class StandardUserEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, StandardUser):
            return {
                "username": o.__getattribute__('_StandardUser__username'),
                "password": o.__getattribute__('_StandardUser__password'),
                'money': o.__getattribute__('_StandardUser__money'),
                'assets': o.__getattribute__('_StandardUser__assets')
            }


def custom_standard_user_decoder(standard_user_dict) -> User:
    return StandardUser(standard_user_dict['username'],
                        standard_user_dict['password'],
                        standard_user_dict['assets'],
                        standard_user_dict['money'])
