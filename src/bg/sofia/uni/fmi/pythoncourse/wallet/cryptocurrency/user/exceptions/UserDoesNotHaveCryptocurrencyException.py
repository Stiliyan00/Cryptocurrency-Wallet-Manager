class UserDoesNotHaveCryptocurrencyException(Exception):
    def __init__(self, offering_code: str):
        message = f'User does not have any amount of cryptocurrency with offering code \'{offering_code}\' to sell!'
        super(UserDoesNotHaveCryptocurrencyException, self).__init__(message)
