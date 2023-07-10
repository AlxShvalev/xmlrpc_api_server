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
    length = random.randint(settings.CHALLENGE_MIN_LENGTH,
                            settings.CHALLENGE_MAX_LENGTH)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def generate_signature(key: int, data: str) -> str:
    signature = hmac.new(bytes(key), data.encode(), hashlib.sha256)
    return signature.hexdigest()


class ServerService:

    def __init__(self, service: DBService) -> None:
        self.__db_service = service

    def get_user(self, username: str, password: str) -> User:
        user = self.__db_service.get_user(username)
        if user is None:
            raise exceptions.UserNotFound(username)
        if user.password != password:
            raise exceptions.IncorrectPassword
        return user

    def __get_session(self, session_id: UUID) -> Session:
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
        secret = session.secret_key
        challenge = session.challenge
        signature = generate_signature(secret, challenge)
        if signature != challenge_signature:
            raise exceptions.IncorrectChallengeSignature
        return challenge

    def create_session(self, user: User) -> str:
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
        return dh_server.public_keys

    def partial_keys_exchange(self, session_id: UUID, client_key: int) -> int:
        session = self.__get_session(session_id)
        session.secret_key = dh_server.generate_full_key(client_key)
        self.__db_service.update_session(session)
        dh_server.generate_partial_key()
        return dh_server.partial_key

    def get_challenge(self, session_id: UUID) -> str:
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
