from abc import ABC, abstractmethod


class Command(ABC):
    @staticmethod
    def help_logging() -> str:
        """
        :return: The allowed commands to a certain user before logging in the app.
        """
        return """
        you can enter commands:
                disconnect
                signup username password
                login username password
        """

    @staticmethod
    def help() -> str:
        """
        :return: The allowed command to a certain user who has already logged in the app
        """
        return """
        you can enter commands:
                disconnect
                get_wallet_summary
                signup <username> <password>
                login <username> <password>
                buy <offering_code>
                sell <offering_code>
                buy <offering_code> <amount>
                deposit <amount_of_money>
                help
                list_offerings
                """

    @abstractmethod
    def get_wallet_summary(self, arguments: list) -> str:
        pass

    @abstractmethod
    def sign_up(self, arguments: list) -> str:
        """
        Allows a certain user to sign up to our SplitWise app.

        :param: arguments An array of argument which contains 2 elements: the username and the password
        which the user has chosen to sing up with.

        :return: [ Unknown command ] if the number of argument is not 2 or
        "successful registration" if the singing up is successful or
        "invalid username" if the chosen username is less than 8 characters or
        "invalid password" if the chosen password is less than 8 characters or
        "username already exists" if there is another user with the chosen username
        """
        pass

    @abstractmethod
    def login(self, arguments: list) -> str:
        """
        :return:    [ Unknown command ] if the number of argument is not 2 or
                    [ "Invalid username" ] if there is no user with the chosen username or
                    an appropriate message for the successful logging in.
        :param arguments: "[ Invalid number of arguments in command login ]" if the number of argument is not 2 or
        an array of argument which contains 2 elements: the username and the password
        which the user has chosen to log in with.
        """
        pass

    @abstractmethod
    def deposit_money(self, arguments: list) -> str:
        """
        :param arguments: An array of argument which contains 2 elements: the amount of money the user
        want to deposit and the username which the user has chosen to log in with.
        :return:    "[ Invalid number of arguments in command deposit ]" if the number of argument is not 2 or
                    an appropriate message for the state of the deposit,
                    "[ Unknown user ]" if the given username is of no existing user in the database,
                    "[ You successfully deposited {money_to_deposit} USD ]" if the user has successfully deposited
                    or an appropriate message for the failure.
        """
        pass

    @abstractmethod
    def list_offerings(self) -> str:
        pass

    @abstractmethod
    def sell(self, arguments: list) -> str:
        """
        :param arguments: An array of argument which contains 2 elements: the cryptocurrency code the user wants to
        sell and the username which the user has chosen to log in with.
        :return:    "[ Invalid number of arguments in command sell ]" if the number of argument
                    is not 2 or an appropriate message for the state of the sell.
                    "[ Unknown user ]" if the given username is of no existing user in the database.
                    "[ You successfully sold {offering_code} for {value} USD ]" if the user has successfully sold the asset.
                    or an appropriate message for the failure.
        """
        pass

    @abstractmethod
    def buy(self, arguments: list):
        """
        :param arguments: An array of argument which contains 3 elements: the cryptocurrency code the user wants to
        buy, the amount of the certain cryptocurrency the user want to buy and the username which the user has
        chosen to log in with.
        :return:    "[ Invalid number of arguments in command sell ]" if the number of argument
                    is not 3 or an appropriate message for the state of the sell,
                    "[ Unknown user ]" if the given username is of no existing user in the database,
                    "[ You successfully bought {amount} of {offering_code} ]" if the user has successfully bought the
                     asset or an appropriate message for the failure.
        """
        pass
