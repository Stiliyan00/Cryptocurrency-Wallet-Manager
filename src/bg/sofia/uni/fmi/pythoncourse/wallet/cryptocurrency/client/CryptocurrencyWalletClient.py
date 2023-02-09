import socket

from src.bg.sofia.uni.fmi.pythoncourse.wallet.cryptocurrency.command.Command import Command


class CryptocurrencyWalletClient:
    SERVER_PORT = 7777  # initiate port no above 1024

    def __init__(self):
        self.__username = ""

    def client_program(self):
        host = socket.gethostname()  # as both code is running on same pc

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, self.SERVER_PORT))  # connect to the server

        if not self.__logging(client_socket):
            client_socket.close()  # close the connection
            return

        message = input(" -> ")  # take input
        while message.lower().strip() != 'disconnect':
            message += f' {self.__username}'
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response

            print(data)  # show in terminal

            message = input(" -> ")  # again take input

        client_socket.send(message.encode())
        client_socket.close()  # close the connection

    def __logging(self, client_socket: socket.socket) -> bool:
        logged_in = False
        message = input(" -> ")  # again take input
        while not logged_in:
            if message.lower().strip() == 'disconnect':
                return False

            if message.lower().strip() == 'help':
                print(Command.help_logging())
                message = input(" -> ")
                continue

            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()

            if data == '[ You successfully logged in ]':
                print(data)
                self.__username = message.split(' ')[1]
                break

            print(data)  # show in terminal
            message = input(" -> ")  # again take input

        return True


CryptocurrencyWalletClient().client_program()
