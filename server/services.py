import hashlib
import hmac
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import exceptions
from DH_encrypt import DHEncrypt
from db.models import Session, User
from db.services import DBService, db_service
from settings import settings


def generate_random_string() -> str:
    length = random.randint(settings.CHALLENGE_MIN_LENGTH,
                            settings.CHALLENGE_MAX_LENGTH)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


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

    def __check_session(self, session: Optional[Session]) -> Session:
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
        signature = hmac.new(bytes(secret), challenge.encode(), hashlib.sha256)
        if signature.hexdigest() != challenge_signature:
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

    def get_secret(self, session_id: UUID, pub_keys: dict) -> int:
        session = self.__db_service.get_session(session_id)
        session = self.__check_session(session)
        try:
            pub_key1 = int(pub_keys["pub_key1"])
            pub_key2 = int(pub_keys["pub_key2"])
            partial_key_client = int(pub_keys["partial_key_client"])
        except:
            raise exceptions.IncorrectPublicKey
        encrypt = DHEncrypt(
            pub_key1,
            pub_key2,
            settings.DH_SECRET_KEY
        )
        partial_key_server = encrypt.generate_partial_key()
        session.secret_key = encrypt.generate_full_key(partial_key_client)
        self.__db_service.update_session(session)
        return partial_key_server

    def get_challenge(self, session: UUID) -> str:
        session = self.__db_service.get_session(session)
        session = self.__check_session(session)
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
        session = self.__db_service.get_session(session_id)
        session = self.__check_session(session)
        self.__check_challenge_signature(
            challenge_signature,
            session
        )
        data = self.__db_service.get_data(data_key)
        return data.data


server_service = ServerService(db_service)
