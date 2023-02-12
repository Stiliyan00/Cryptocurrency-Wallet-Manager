from __future__ import annotations

from abc import ABC, abstractmethod


class User(ABC):

    @abstractmethod
    def deposit_money(self, amount: float):
        """
        Allows the current user to top up a certain amount of USA dollars into his/her wallet.
        :param amount: The amount of money which the current user wants to add to his/her wallet.
        :raise ValueError: If the amount of money to be depositing is less or equal to 0 USD.
        """
        pass

    @abstractmethod
    def buy(self, offering_code: str, amount: float):
        """
        Allows the current user to bull a certain amount of a certain cryptocurrency, if there is enough deposit money
        in his/her wallet.
        :param offering_code: The code of the cryptocurrency which the current user wants to buy.
        :param amount: The amount of the cryptocurrency which the current user wants to buy.
        :raise NotEnoughMoneyError: If the current user does not have enough money to buy the wanted amount of the
        wanted cryptocurrency.
        :raise CryptocurrencyDoesNotExistException: If the passed offering_code is of no existing cryptocurrency.
        :raise ValueError: If the amount of the cryptocurrency to be bought is less or equal to 0.
        """
        pass

    @abstractmethod
    def sell(self, offering_code: str) -> float:
        """
        Allows the current user to sell all the amount of a certain cryptocurrency.
        :param offering_code: The code of the cryptocurrency which the current user wants to sell.
        :return: The value of the cryptocurrency the users has sold.
        :raise UserDoesNotHaveCryptocurrencyException: If the current user does not possess the cryptocurrency
        """
        pass

    @abstractmethod
    def is_valid_password(self, password: str) -> bool:
        """
        :param password: The currently inputted password.
        :return: true if the value of password1 equals the current user's password value
        """
        pass

    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def get_money(self) -> float:
        pass

    @abstractmethod
    def get_assets(self) -> dict:
        pass
