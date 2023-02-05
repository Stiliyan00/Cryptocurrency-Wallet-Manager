from abc import ABC, abstractmethod

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User


class CryptocurrencyWallet(ABC):
    @abstractmethod
    def find_user_by_username(self, username: str) -> User:
        """
        @param username The user's username we want to find in our database of username.
        @return The user with this username.
        """
    @abstractmethod
    def register(self, username: str, password: str):
        """
        Allow a new user to make a registration in CryptocurrencyWallet with username {@code username} and
        with password {@code password}.
        @param username: The username which the new user has chosen
        @param password: The password which the new user has chosen
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
        @param username The username of the user we are searching information of.
        @return Full information of all current investments and the money of a certain user.
        """
        pass

    @abstractmethod
    def list_offerings(self) -> dict:
        """
        Allow the current user to see all available cryptocurrencies at the moment, which he/she may or may not
        want to buy. The information is from CoinAPI (https://www.coinapi.io).
        @return Returns a dictionary of all currently available cryptocurrencies and their prices.
        """
        pass

    @abstractmethod
    def get_wallet_overall_summary(self) -> str:
        """
        Allows the current user to get information all his current investments, by comparing the price of every single
        cryptocurrency which the user has bought and its current price.

        @return Returns an info string representation of the full winnings/lost report of all current investments of
        the current user.
        """
        pass
