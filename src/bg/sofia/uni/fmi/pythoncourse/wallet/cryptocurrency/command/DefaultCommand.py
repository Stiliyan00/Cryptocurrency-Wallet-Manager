import json

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.CryptocurrencyWallet import CryptocurrencyWallet
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.command.Command import Command
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.PasswordIsNotCorrectException import \
    PasswordIsNotCorrectException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.UserAlreadyExistsException import \
    UserAlreadyExistsException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.exceptions.UserDoesNotExistException import \
    UserDoesNotExistException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.User import User
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.CryptocurrencyDoesNotExistException import \
    CryptocurrencyDoesNotExistException
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.NotEnoughMoneyError import \
    NotEnoughMoneyError
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.user.exceptions.UserDoesNotHaveCryptocurrencyException import \
    UserDoesNotHaveCryptocurrencyException


class DefaultCommand(Command):

    def __init__(self, wallet: CryptocurrencyWallet):
        self.__wallet = wallet

    def list_offerings(self) -> str:
        return json.dumps(self.__wallet.list_offerings(), sort_keys=True, indent=4)

    def get_wallet_summary(self, arguments: list) -> str:
        if len(arguments) != 1:
            return '[ Unknown command ]'
        #     The only argument to be passed should be a username:
        try:
            return self.__wallet.get_wallet_summary(arguments[len(arguments) - 1])
        except UserDoesNotExistException:
            return f'[ No such user with username {arguments[len(arguments) - 1]} ]'

    def sign_up(self, arguments: list) -> str:
        if len(arguments) != 2:
            return '[ Unknown command ]'
        try:
            self.__wallet.register(arguments[0], arguments[1])
            return '[ successful registration ]'
        except ValueError:
            return f'[ Invalid username or password ]'
        except UserAlreadyExistsException:
            return '[ username already exists ]'

    def login(self, arguments: list) -> str:
        if len(arguments) != 2:
            return '[ Unknown command ]'
        try:
            self.__wallet.login(arguments[0], arguments[1])
            return '[ You successfully logged in ]'
        except ValueError:
            return '[ Invalid username or password ]'
        except PasswordIsNotCorrectException:
            return '[ Incorrect password ]'
        except UserAlreadyExistsException:
            return '[ username already exists ]'

    def deposit_money(self, arguments: list) -> str:
        if len(arguments) != 2:
            return '[ Unknown command ]'
        money_to_deposit: float = float(arguments[0])
        username: str = arguments[1]
        user: User = self.__wallet.find_user_by_username(username)
        if user is None:
            return '[ Unknown user ]'
        try:
            user.deposit_money(money_to_deposit)
            return f'[ You successfully deposited {money_to_deposit} USD ]'
        except ValueError as e:
            return str(e)

    def sell(self, arguments: list) -> str:
        if len(arguments) != 2:
            return '[ Unknown command ]'
        username: str = arguments[1]
        offering_code: str = arguments[0]
        user: User = self.__wallet.find_user_by_username(username)
        if user is None:
            return '[ Unknown user ]'
        try:
            value = user.sell(offering_code)
            return f'[ You successfully sold {offering_code} for {value} USD ]'
        except UserDoesNotHaveCryptocurrencyException as e:
            return str(e)

    def buy(self, arguments: list):
        if len(arguments) != 3:
            return '[ Unknown command ]'
        username: str = arguments[2]
        offering_code: str = arguments[0]
        amount: float = float(arguments[1])

        user: User = self.__wallet.find_user_by_username(username)
        if user is None:
            return '[ Unknown user ]'
        try:
            value = user.buy(offering_code, amount)
            return f'[ You successfully bought {value} of {offering_code} ]'
        except ValueError as e:
            return str(e)
        except CryptocurrencyDoesNotExistException as e:
            return str(e)
        except NotEnoughMoneyError as e:
            return str(e)
