from typing import Dict

from bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.repository.CryptocurrencyCoinsAPIClient import \
    CryptocurrencyCoinsAPIClient
from bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User
from bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.NotEnoughMoneyError import NotEnoughMoneyError


class StandardUser(User):
    PASSWORD_MINIMUM_LENGTH = 8
    PASSWORD_SPECIAL_SYMBOLS = ['@', '%', '#', '!', '*', '-', '_']

    def __init__(self, username: str, password: str, assets: dict):
        self.__validate_username(username)
        self.__validate_password(password)
        self.__username = username
        self.__password = password
        self.__money = 0
        self.__assets = assets

    def __validate_username(self, username: str):
        #     TODO("to check in the data base if the username is taken or not!")
        if not username or not username.strip():
            raise ValueError('Invalid username! Username cannot be an empty string')

    def __validate_password(self, password: str):
        if not password or not password.strip():
            raise ValueError('Invalid password! Password cannot be an empty string!')

        if len(password) < self.PASSWORD_MINIMUM_LENGTH:
            raise ValueError('Invalid password! Password but be at least 8 symbols!')

        if len(list(filter(lambda x: x in StandardUser.PASSWORD_SPECIAL_SYMBOLS, list(password)))) == 0:
            ValueError('Invalid password! Password should contain at least one symbol from the '
                       'following: ' + self.PASSWORD_SPECIAL_SYMBOLS.__str__())

    def __cryptocurrency_exists(self, offering_code)-> bool:
        return CryptocurrencyCoinsAPIClient.get_specific_rate_of_currency()

    def deposit_money(self, amount: float):
        if amount <= 0.0:
            raise ValueError('Invalid amount for deposit! You cannot deposit 0 or less dollars!')
        self.__money += amount

    def list_offerings(self) -> Dict[str, float]:
        json_str = CryptocurrencyCoinsAPIClient.get_list_of_all_assets().json()
        result = dict()
        for i in json_str:
            # not optimal at all
            if i['type_is_crypto'] == 1:
                price_usd = \
                    CryptocurrencyCoinsAPIClient.get_specific_rate_of_currency(i['asset_id'], 'USD').json()['rate']
                result[i['asset_id']] = price_usd
        return result

    def buy(self, offering_code: str, amount: float):
        # The amount is the money not the asset
        if amount <= 0.0:
            raise ValueError('The wanted cryptocurrency ' + offering_code + ' cannot be 0.0 or less!')
        if amount > self.__money:
            raise NotEnoughMoneyError(amount)
        if
        if self.__assets.get(offering_code) == None:
            self.__assets[offering_code]

    def sell(self, offering_code: str):
        pass

    def is_valid_password(self, password: str) -> bool:
        return password == self.__password
