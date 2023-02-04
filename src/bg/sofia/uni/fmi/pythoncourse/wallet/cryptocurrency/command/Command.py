from abc import ABC


class Command(ABC):
    @staticmethod
    def help_logging() -> str:
        """
        @return: The allowed commands to a certain user before logging in the app.
        """
        return """
        you can enter commands:
                disconnect
                signup username password
                login username password
        """

    @staticmethod
    def help() -> str:
        """
        @return: The allowed command to a certain user who has already logged in the app
        """
        return """
        you can enter commands:
                disconnect
                my-status
                ...
        """
