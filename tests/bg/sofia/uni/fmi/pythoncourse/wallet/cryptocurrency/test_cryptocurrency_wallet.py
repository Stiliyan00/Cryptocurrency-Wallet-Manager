import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pytest

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.DefautCryptocurrencyWallet import \
    DefaultCryptocurrencyWallet
from tests.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.test_user import mocked_requests_get


class MyTestCase(unittest.TestCase):
    TEMPORARY_DIRECTORY_PATH = tempfile.TemporaryDirectory().name

    def test_should_always_pass(self):
        self.assertTrue(True)  # add assertion here

    def test_cryptocurrency_wallet_constructor_with_invalid_string_for_file_path(self):
        invalid_file_path = ""
        with pytest.raises(ValueError):
            DefaultCryptocurrencyWallet(invalid_file_path)

        invalid_file_path2 = None
        with pytest.raises(ValueError):
            DefaultCryptocurrencyWallet(invalid_file_path2)

    def test_cryptocurrency_wallet_constructor_with_none_existing_file_path(self):
        invalid_file_path = "random_invalid_file_path"
        with pytest.raises(FileExistsError):
            DefaultCryptocurrencyWallet(invalid_file_path)

    def test_cryptocurrency_wallet_constructor_with_valid_file_path(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_dir = Path(tmpdirname)
            print(temp_dir, temp_dir.exists())
            file_name = temp_dir / "test.txt"

            print(file_name, file_name.exists())
            # DefaultCryptocurrencyWallet(file_name.__str__())


if __name__ == '__main__':
    unittest.main()
