class CryptocurrencyDoesNotExistException(Exception):
    def __init__(self, offering_code: str):
        message = f'Cryptocurrency with offering code \'{offering_code}\' does not exist!'
        super(CryptocurrencyDoesNotExistException, self).__init__(message)
