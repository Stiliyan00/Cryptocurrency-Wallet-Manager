import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pytest

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.DefautCryptocurrencyWallet import \
    DefaultCryptocurrencyWallet
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.UserAlreadyExistsException import \
    UserAlreadyExistsException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.UserDoesNotExistException import \
    UserDoesNotExistException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.StandardUser import StandardUser
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User
from tests.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.test_user import mocked_requests_get


class MyTestCase(unittest.TestCase):
    TEMPORARY_DATA_FILE_PATH = os.path.join('temporary_test_file_data.txt')
    user1: User = StandardUser(username='stiliyan', password='password1', assets={}, money=10000)
    user2: User = StandardUser(username='teodor', password='password2', assets={}, money=12000)
    user3: User = StandardUser(username='kris', password='password3', assets={}, money=15000)

    def setUp(self) -> None:
        users_list = list()
        users_list.append(dict(self.user1))
        users_list.append(dict(self.user2))
        users_list.append(dict(self.user3))

        users_json = json.dumps(users_list, indent=4)

        with open(self.TEMPORARY_DATA_FILE_PATH, "w") as f:
            f.write(users_json)

    def tearDown(self) -> None:
        with open(self.TEMPORARY_DATA_FILE_PATH, 'w') as f:
            f.close()

    def test_should_always_pass(self):
        self.assertTrue(True)  # add assertion here

    def test_cryptocurrency_wallet_constructor_with_invalid_string_for_file_path_should_raise_exception(self):
        invalid_file_path = ""
        with pytest.raises(ValueError):
            DefaultCryptocurrencyWallet(invalid_file_path)

        invalid_file_path2 = None
        with pytest.raises(ValueError):
            DefaultCryptocurrencyWallet(invalid_file_path2)

    def test_cryptocurrency_wallet_constructor_with_none_existing_file_path_should_raise_exception(self):
        invalid_file_path = "random_invalid_file_path"
        with pytest.raises(FileExistsError):
            DefaultCryptocurrencyWallet(invalid_file_path)

    def test_cryptocurrency_wallet_constructor_with_invalid_data_should_raise_exception(self):
        invalid_data = [
            """[{
                "username": "stiliyan",
                "password": "password1",
                "money": 4347.426291494547
            }]""",
            'invalid_data',
            """[{
                "password": "password1",
                "money": 4347.426291494547,
                "assets": {
                    "BTC": 3.1
                }
            }]"""
        ]
        for i in invalid_data:
            # Clear the data from the setUp:
            with open(self.TEMPORARY_DATA_FILE_PATH, 'w') as f:
                f.close()

            # Write the invalid data in the file:
            with open(self.TEMPORARY_DATA_FILE_PATH, "w") as f:
                f.write(i)

            with pytest.raises(ValueError):
                DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

    def test_cryptocurrency_wallet_constructor_with_valid_file_path(self):
        DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

    def test_find_user_with_none_existing_users_username(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)
        assert wallet.find_user_by_username('none_existing_user') is None

    def test_find_user_with_existing_user_username(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)
        assert wallet.find_user_by_username('stiliyan').__eq__(self.user1)

    def test_register_with_empty_string_for_username_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        with pytest.raises(ValueError):
            wallet.register(None, "#password1")

        with pytest.raises(ValueError):
            wallet.register('', "@password1")

        with pytest.raises(ValueError):
            wallet.register(' ', "@password1")

    def test_register_with_existing_user_username_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        with pytest.raises(UserAlreadyExistsException):
            wallet.register('stiliyan', "@password1")

    def test_register_with_invalid_username_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        with pytest.raises(ValueError):
            wallet.register('notLong', "@password1")

    def test_register_with_empty_string_password_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        with pytest.raises(ValueError):
            wallet.register("stiliyan1", None)

        with pytest.raises(ValueError):
            wallet.register("stiliyan1", '')

        with pytest.raises(ValueError):
            wallet.register("stiliyan1", ' ')

    def test_register_with_not_long_enough_password_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        with pytest.raises(ValueError):
            wallet.register("stiliyan1", "@pass#")

    def test_register_with_no_special_symbols_in_password_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        with pytest.raises(ValueError):
            wallet.register("stiliyan1", "password1")

    def test_register_with_valid_username_and_password(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        username = 'viktor123'
        password = '#password4@'
        # Register the user:
        wallet.register(username=username, password=password)

        # Assert the user was created successfully:
        user = wallet.find_user_by_username('viktor123')
        assert user.is_valid_password(password)
        assert user.get_username() == username
        assert user.get_money() == 0
        assert user.get_assets().__eq__(dict())

    def test_get_wallet_summary_with_none_existing_user_username_should_raise_exception(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        username = 'non_existing_username'

        with pytest.raises(UserDoesNotExistException):
            wallet.get_wallet_summary(username)

    def test_get_wallet_summary_with_existing_user_username(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        username = self.user1.get_username()

        get_wallet_summary_expected_result = \
            {'money': self.user1.get_money(), 'investments': self.user1.get_assets()}.__str__()

        assert wallet.get_wallet_summary(username) == get_wallet_summary_expected_result

    def test_get_all_users(self):
        wallet = DefaultCryptocurrencyWallet(self.TEMPORARY_DATA_FILE_PATH)

        expected_user_set = set()
        expected_user_set.add(self.user1)
        expected_user_set.add(self.user2)
        expected_user_set.add(self.user3)

        wallet_get_all_users_actual_result = wallet.get_all_users()

        # Assert the user set:
        assert len(expected_user_set) == len(wallet_get_all_users_actual_result)
        assert all(elem in expected_user_set for elem in wallet_get_all_users_actual_result)

        # Assert the actual user set is a copy:
        wallet_get_all_users_actual_result.add(StandardUser('Dimitar12', "#password5@", {}))
        assert len(wallet_get_all_users_actual_result) != len(expected_user_set)


if __name__ == '__main__':
    unittest.main()
