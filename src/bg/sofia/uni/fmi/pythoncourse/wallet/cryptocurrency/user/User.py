from __future__ import annotations

import json
from abc import ABC, abstractmethod

from typing import Dict


class User(ABC):

    @staticmethod
    def of(line: str) -> User:
        """
        Allows 1 line of our database to be parsed to a User object.
        """
        if not str:
            raise ValueError('The value of argument line in static method of in class User is invalid.')
        user_json_dict = json.loads(line)

        return

    @abstractmethod
    def deposit_money(self, amount: float):
        """
        Allows the current user to top up a certain amount of USA dollars into his/her wallet.
        @param amount: The amount of money which the current user wants to add to his/her wallet.
        """
        pass

    @abstractmethod
    def list_offerings(self) -> Dict[str, float]:
        """
        Allow the current user to see all available cryptocurrencies at the moment, which he/she may or may not
        want to buy. The information is from CoinAPI (https://www.coinapi.io).
        @return Returns a dictionary of all currently available cryptocurrencies and their prices.
        """
        pass

    @abstractmethod
    def buy(self, offering_code: str, amount: float):
        """
        Allows the current user to bull a certain amount of a certain cryptocurrency, if there is enough deposit money
        in his/her wallet.
        @param offering_code: The code of the cryptocurrency which the current user wants to buy.
        @param amount: The amount of the cryptocurrency which the current user wants to buy.
        """
        pass

    @abstractmethod
    def sell(self, offering_code: str):
        """
        Allows the current user to sell all the amount of a certain cryptocurrency.
        @param offering_code: The code of the cryptocurrency which the current user wants to sell.
        """
        pass

    @abstractmethod
    def is_valid_password(self, password: str) -> bool:
        """
        @param password: The currently inputted password.
        @return: true if the value of password1 equals the current user's password value
        """
        pass