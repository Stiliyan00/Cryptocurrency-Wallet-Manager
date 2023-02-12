import json
import os
from datetime import datetime, date

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.CryptocurrencyWallet import CryptocurrencyWallet
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.PasswordIsNotCorrectException import \
    PasswordIsNotCorrectException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.UserAlreadyExistsException import \
    UserAlreadyExistsException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.UserDoesNotExistException import \
    UserDoesNotExistException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.repository.CryptocurrencyCoinsAPIClient import \
    CryptocurrencyCoinsAPIClient
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.StandardUser import custom_standard_user_decoder, \
    StandardUser
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User


class DefaultCryptocurrencyWallet(CryptocurrencyWallet):
    PASSWORD_MINIMUM_LENGTH = 8
    PASSWORD_SPECIAL_SYMBOLS = ['@', '%', '#', '!', '*', '-', '_']

    def __init__(self, file_path: str):
        self.__users_set = set()
        if not file_path:
            raise ValueError('The argument of the constructor cannot be None!')
        if not os.path.exists(file_path):
            raise FileExistsError(f'The given file path {file_path} does not exist!')
        try:
            self.user_data_path = file_path
            users_data_file = open(file_path, 'r')
            users_data_json = json.loads(users_data_file.read())
            for user_str in users_data_json:
                temp_user: User = custom_standard_user_decoder(user_str)
                self.__users_set.add(temp_user)
        except json.decoder.JSONDecodeError and KeyError:
            raise ValueError('Invalid data in database!')

    def __validate_username(self, username: str):
        if not username or not username.strip():
            raise ValueError('Invalid username! Username cannot be an empty string')
        if self.find_user_by_username(username) is not None:
            raise UserAlreadyExistsException(username)
        if len(username) < 8:
            raise ValueError('Invalid username! Username should be at least 8 symbols long!')

    def __validate_password(self, password: str):
        if not password or not password.strip():
            raise ValueError('Invalid password! Password cannot be an empty string!')

        if len(password) < self.PASSWORD_MINIMUM_LENGTH:
            raise ValueError('Invalid password! Password but be at least 8 symbols!')

        if not any(x in list(password) for x in DefaultCryptocurrencyWallet.PASSWORD_SPECIAL_SYMBOLS):
            raise ValueError('Invalid password! Password should contain at least one symbol from the following: ' +
                             DefaultCryptocurrencyWallet.PASSWORD_SPECIAL_SYMBOLS.__str__())

    def find_user_by_username(self, username: str):
        if not username:
            return None
        for user in self.__users_set:
            if user.get_username() == username:
                return user
        return None

    def register(self, username: str, password: str):
        self.__validate_username(username)
        self.__validate_password(password)
        self.__users_set.add(StandardUser(username, password, {}))

    def login(self, username: str, password: str) -> User:
        if not username:
            raise ValueError('The username cannot be None or an empty string.')
        if not password:
            raise ValueError('The password cannot be None or an empty string.')
        user = self.find_user_by_username(username)
        if user is None:
            raise UserDoesNotExistException
        if not user.is_valid_password(password):
            raise PasswordIsNotCorrectException(username, password)
        return user

    def store_users_data(self):
        # TODO("To think of a better way to store the data than first parsing the set of users to a user list of dicts")
        users_list = list()
        for user in self.__users_set:
            users_list.append(dict(user))

        users_json = json.dumps(users_list, indent=4)
        with open(self.user_data_path, 'w') as fp:
            fp.write(users_json)

    def get_wallet_summary(self, username: str) -> str:
        user = self.find_user_by_username(username)
        if user is None:
            raise UserDoesNotExistException(username)
        return {
            'money': user.get_money(),
            'investments': user.get_assets()
        }.__str__()

    def list_offerings(self) -> dict:
        json_str = CryptocurrencyCoinsAPIClient.get_list_of_all_assets().json()
        result = dict()
        for i in json_str:
            # not optimal at all
            date_object = datetime.strptime(i['data_end'], '%Y-%m-%d').date()
            if i['type_is_crypto'] == 1 and not date_object < datetime.strptime(date.today().__str__(),
                                                                                '%Y-%m-%d').date():
                try:
                    price_usd = \
                        CryptocurrencyCoinsAPIClient.get_specific_rate_of_currency(i['asset_id'], 'USD').json()['rate']
                    result[i['asset_id']] = price_usd
                except KeyError:
                    pass
        return result

    def get_wallet_overall_summary(self) -> str:
        pass

    def get_all_users(self) -> set:
        return self.__users_set.copy()
