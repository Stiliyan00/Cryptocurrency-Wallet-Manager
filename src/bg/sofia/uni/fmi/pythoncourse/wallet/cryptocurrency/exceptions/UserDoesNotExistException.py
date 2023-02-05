class UserDoesNotExistException(Exception):
    def __init__(self, username: str):
        message = f'The user with username \'{username}\' does not exist!'
        super(UserDoesNotExistException, self).__init__(message)
