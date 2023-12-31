import hashlib
import hmac
import random
import string
from datetime import datetime, timedelta
from typing import Dict
from uuid import UUID

import exceptions
from db.models import Session, User
from db.services import DBService, db_service
from dh_algorithm import dh_server
from settings import settings


def generate_random_string() -> str:
    """Generate random string."""
    length = random.randint(settings.CHALLENGE_MIN_LENGTH,
                            settings.CHALLENGE_MAX_LENGTH)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def generate_signature(key: bytes, data: str) -> str:
    """Generate signature for data by key."""
    signature = hmac.new(bytes(key), data.encode(), hashlib.sha256)
    return signature.hexdigest()


class ServerService:
    """Class for inner server business-logic."""

    def __init__(self, service: DBService) -> None:
        self.__db_service = service

    def rester_user(self, username: str, password: str) -> str:
        """Register user if not exists. Create session for new user. Return session id."""
        user = self.__db_service.get_user(username)
        if user:
            print(user)
            raise exceptions.UserAlreadyExists(username)
        hashed_password = generate_signature(settings.SECRET_KEY.encode(), password)
        user = User(username=username, password=hashed_password)
        user = self.__db_service.create_user(user)
        return self.create_session(user)

    def get_user(self, username: str, password: str) -> User:
        """Get user from DB. If user is not found or password is incorrect, raise exception."""
        user = self.__db_service.get_user(username)
        if user is None:
            raise exceptions.UserNotFound(username)
        hashed_password = generate_signature(settings.SECRET_KEY.encode(), password)
        if hashed_password != user.password:
            raise exceptions.IncorrectPassword
        return user

    def __get_session(self, session_id: UUID) -> Session:
        """Get session from db. If session is not found or session is expired, raise exception."""
        session = self.__db_service.get_session(session_id)
        if session is None:
            raise exceptions.IncorrectSession
        if session.expired_date < datetime.now():
            self.__db_service.delete_session(session)
            raise exceptions.SessionIsExpired
        return session

    def __check_challenge_signature(
            self,
            challenge_signature: str,
            session: Session
    ):
        """Check challenge signature by secret. If signature is incorrect, raise exception."""
        secret = bytes(session.secret_key)
        challenge = session.challenge
        signature = generate_signature(secret, challenge)
        if signature != challenge_signature:
            raise exceptions.IncorrectChallengeSignature
        return challenge

    def create_session(self, user: User) -> str:
        """Check session for user. If session is exists, return it id.
         Else create new session and return it id.
         """
        session = self.__db_service.get_session_by_user_id(user.id)
        if session:
            return str(session.id)
        session = Session(
            user_id=user.id,
            expired_date=(datetime.now() +
                          timedelta(seconds=settings.SESSION_LIFETIME),)
        )
        session = self.__db_service.create_session(session)
        return str(session.id)

    def get_pub_keys(self) -> Dict[str, int]:
        """Get session public key."""
        return dh_server.public_keys

    def partial_keys_exchange(self, session_id: UUID, client_key: int) -> int:
        """Generate full key for user and save it into DB. Return server partial key."""
        session = self.__get_session(session_id)
        session.secret_key = dh_server.generate_full_key(client_key)
        self.__db_service.update_session(session)
        dh_server.generate_partial_key()
        return dh_server.partial_key

    def get_challenge(self, session_id: UUID) -> str:
        """Generate random challenge string, save it into DB and return it."""
        session = self.__get_session(session_id)
        challenge = generate_random_string()
        session.challenge = challenge
        self.__db_service.update_session(session)
        return challenge

    def get_data(
            self,
            session_id: UUID,
            data_key: str,
            challenge_signature: string
    ) -> str:
        """Check user challenge signature by user secret key.
        If success, return date from DB by data key. If data not exists, raise exception."""
        session = self.__get_session(session_id)
        self.__check_challenge_signature(
            challenge_signature,
            session
        )
        data = self.__db_service.get_data(data_key)
        if data is None:
            raise exceptions.DataNotFound(data_key)
        return data.data


server_service = ServerService(db_service)
