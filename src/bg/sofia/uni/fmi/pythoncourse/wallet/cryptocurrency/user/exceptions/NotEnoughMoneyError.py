class NotEnoughMoneyError(Exception):
    def __init__(self, money: float, message='Not enough money in your CryptoWallet at this moment!'):
        self.money = money
        super(NotEnoughMoneyError, self).__init__(message)
