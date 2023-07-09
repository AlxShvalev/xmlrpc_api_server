class Error(Exception):
    """Base cless for error messages"""
    detail: str = "Какая-то неизвестная ошибка."

    def __str__(self):
        return self.detail

    def __repr__(self):
        return self.__str__()


class UserNotFound(Error):
    def __init__(self, username: str) -> None:
        self.detail = f"Пользователь c username '{username}' не найден."


class IncorrectPassword(Error):
    detail = "Invalid password."


class SessionIsExpired(Error):
    detail = "Session is expired. Please Sign in again."


class IncorrectSession(Error):
    detail = "Session id is incorrect."


class IncorrectChallengeSignature(Error):
    detail = "Incorrect challenge signature. Authorization failed."


class IncorrectPublicKey(Error):
    detail = "Required public keys are missing or not integer."
