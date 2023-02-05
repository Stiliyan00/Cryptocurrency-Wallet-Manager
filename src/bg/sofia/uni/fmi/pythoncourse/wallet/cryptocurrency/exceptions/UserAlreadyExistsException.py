class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        message = f'The user with username \'{username}\' already exists!'
        super(UserAlreadyExistsException, self).__init__(message)
