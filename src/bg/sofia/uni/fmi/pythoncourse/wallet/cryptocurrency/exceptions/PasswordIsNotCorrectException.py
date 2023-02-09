class PasswordIsNotCorrectException(Exception):
    def __init__(self, username: str, password: str):
        message = f'There is no user with username \'{username}\' and password \'{password}\'!'
        super(PasswordIsNotCorrectException, self).__init__(message)