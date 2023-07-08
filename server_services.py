import random
import string
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

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
            raise Exception("User not found.")
        if user.password != password:
            raise Exception("Password incorrect.")
        return user

    def __check_session(self, session: Optional[Session]) -> Session:
        if session is None:
            raise Exception("Session id is incorrect.")
        if session.expired_date < datetime.now():
            self.__db_service.delete_session(session)
            raise Exception("Session is expired. Please sign in again.")
        return session

    def create_session(self, user: User) -> str:
        session = self.__db_service.get_session_by_user_id(user.id)
        if session:
            return str(session.id)
        session = Session(
            user_id=user.id,
            expired_date=datetime.now() + timedelta(seconds=settings.SESSION_LIFETIME),
        )
        session = self.__db_service.create_session(session)
        return str(session.id)

    def get_partial_key(self, session_id: UUID, pub_keys: dict) -> int:
        session = self.__db_service.get_session(session_id)
        session = self.__check_session(session)
        if session.partial_key_server:
            return session.partial_key_server
        try:
            session.pub_key_1 = int(pub_keys["pub_key1"])
            session.pub_key_2 = int(pub_keys["pub_key2"])
            session.partial_key_client = int(pub_keys["partial_key_client"])
        except:
            raise Exception("Required public keys are missing or not integer.")
        encrypt = DHEncrypt(
            session.pub_key_1,
            session.pub_key_2,
            settings.DH_SECRET_KEY
        )
        session.partial_key_server = encrypt.generate_partial_key()
        session = self.__db_service.update_session(session)
        return session.partial_key_server

    def get_challenge(self, session: UUID) -> str:
        session = self.__db_service.get_session(session)
        session = self.__check_session(session)
        if session.challenge:
            return session.challenge
        challenge = generate_random_string()
        session.challenge = challenge
        self.__db_service.update_session(session)
        return challenge


server_service = ServerService(db_service)
