import os
import socket

from _thread import *
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.CryptocurrencyWallet import CryptocurrencyWallet
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.DefautCryptocurrencyWallet import \
    DefaultCryptocurrencyWallet
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.command.Command import Command
from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.command.DefaultCommand import DefaultCommand


class CryptocurrencyWalletServer:
    SERVER_PORT = 7777  # initiate port no above 1024
    UNKNOWN_COMMAND = "[ Unknown command ]"
    MESSAGE_COMMAND_INDEX = 0
    USER_DATA_PATH = os.path.join('..', '..', '..', '..', '..', '..', '..', '..', '..', 'data', 'users_data.txt')

    def __init__(self):
        self.__currently_logged_users = list()
        self.__wallet: CryptocurrencyWallet = DefaultCryptocurrencyWallet(self.USER_DATA_PATH)
        self.__command: Command = DefaultCommand(self.__wallet)

    def multi_threaded_client(self, connection, address):
        while True:
            data = connection.recv(1024).decode()
            if not data:
                break
            print("Message [", data, "] received from client ", address)
            response = self.handle_key_is_readable(data)
            connection.send(response.encode())
        connection.close()

    def start(self):
        host = socket.gethostname()

        server_socket = socket.socket()  # get instance
        try:
            server_socket.bind((host, self.SERVER_PORT))  # bind host address and port together
        except socket.error as e:
            print(str(e))

        # configure how many client the server can listen simultaneously
        server_socket.listen(5)
        while True:
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            # receive data stream. it won't accept data packet greater than 1024 bytes
            start_new_thread(self.multi_threaded_client, (conn, address, ))

        self.__wallet.store_users_data()
        conn.close()  # close the connection

    def stop(self):
        pass

    def check_if_user_is_already_logged(self, username: str) -> bool:
        return username in self.__currently_logged_users

    def handle_key_is_readable(self, data: str) -> str:
        if not data:
            return self.UNKNOWN_COMMAND

        command: str = data.split(' ')[self.MESSAGE_COMMAND_INDEX]
        arguments = data.split(' ')
        arguments.pop(0)  # Removing command str from data

        if command == 'signup':
            return self.__command.sign_up(arguments)
        elif command == 'login':
            username = arguments[0]
            if self.check_if_user_is_already_logged(username):
                return '[ User already logged in ]'
            self.__currently_logged_users.append(username)
            return self.__command.login(arguments)
        elif command == 'buy':
            return self.__command.buy(arguments)
        elif command == 'sell':
            return self.__command.sell(arguments)
        elif command == 'deposit':
            return self.__command.deposit_money(arguments)
        elif command == 'help':
            return Command.help()
        elif command == 'get_wallet_summary':
            return self.__command.get_wallet_summary(arguments)
        elif command == 'list_offerings':
            return self.__command.list_offerings()
        elif command == 'get_asset_info':
            return self.__command.get_asset_info(arguments[0])
        # TODO()
        # This should not be like this because we should store the data only if the server is disconnected but not
        # is a single user is disconnected
        elif command == 'disconnect':
            username = arguments[0]
            self.__currently_logged_users.remove(username)
            return ""
        else:
            return self.UNKNOWN_COMMAND


CryptocurrencyWalletServer().start()
