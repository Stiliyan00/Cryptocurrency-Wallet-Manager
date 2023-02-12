from abc import ABC, abstractmethod

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User


class CryptocurrencyWallet(ABC):
    @abstractmethod
    def find_user_by_username(self, username: str) -> User:
        """
        :param username The user's username we want to find in our database of username.
        :return: The user with this username or None if there is no such user.
        """

    @abstractmethod
    def register(self, username: str, password: str):
        """
        Allow a new user to make a registration in CryptocurrencyWallet with username {@username} and
        with password {@password}.
        :param  username: The username which the new user has chosen
        :param  password: The password which the new user has chosen
        :raises  ValueError: If username is less than 8 symbols/username is not a valid string or password is
        not a valid string/less than 8 symbols/does not contain a special symbol.
        :raises UserAlreadyExistsException: If a user with this username already exists.
        """
        pass

    @abstractmethod
    def store_users_data(self):
        """
        Stores the current data in our database.
        """
        pass

    @abstractmethod
    def get_wallet_summary(self, username: str) -> str:
        """
        :param username The username of the user we are searching information of.
        :return: Full information of all current investments and the money of a certain user.
        :raise UserDoesNotExistException: If a user with username {@username} does not exist in the database.
        """
        pass

    @abstractmethod
    def list_offerings(self) -> dict:
        """
        Allow the current user to see all available cryptocurrencies at the moment, which he/she may or may not
        want to buy. The information is from CoinAPI (https://www.coinapi.io).
        :return: Returns a dictionary of all currently available cryptocurrencies and their prices.
        """
        pass

    @abstractmethod
    def get_wallet_overall_summary(self) -> str:
        """
        Allows the current user to get information all his current investments, by comparing the price of every single
        cryptocurrency which the user has bought and its current price.

        :return: Returns an info string representation of the full winnings/lost report of all current investments of
        the current user.
        """
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> User:
        """
        Allows the user with username {@username} to log-in to the wallet.
        :param username: The username of the user which is trying to log in.
        :param password: The password of the user which is trying to log in.
        :rtype: User
        :return: The user object of the current user.
        :raise ValueError: If the username or the password is not a valid string.
        :raise UserDoesNotExistException: If there is no such user in the database.
        :raise PasswordIsNotCorrectException: If the password is not correct for this user.
        """
        pass
