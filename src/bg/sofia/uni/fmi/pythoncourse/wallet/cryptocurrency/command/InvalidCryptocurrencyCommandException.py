class InvalidCryptocurrencyCommandException(Exception):
    def __init__(self, command: str):
        message = f'There is no such command as \'{command}\'!'
        super(InvalidCryptocurrencyCommandException, self).__init__(message)
