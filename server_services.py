from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from DH_encrypt import DHEncrypt
from db.models import Session, User
from db.services import DBService, db_service
from settings import settings

class ServerService:

    def __init__(self, db_service: DBService) -> None:
        self.__db_service = db_service

    def get_user(self, username: str) -> User:
        return self.__db_service.get_user(username)

    def create_session(self, user: User) -> UUID:
        session = Session(
            user_id=user.id,
            expired_date=datetime.now() + timedelta(settings.SESSION_LIFETIME),
        )
        session = self.__db_service.create_session(session)
        print("session =", session)
        return session.id

    def __session_is_expired(self, session: Session) -> bool:
        return True if session.expired_date < datetime.now() else False

    def get_partial_key(self, session_id: UUID, pub_keys: dict) -> int:
        session = self.__db_service.get_session(session_id)
        if self.__session_is_expired(session):
            return "Session is expired. Please sign in again."
        try:
            session.pub_key_1 = int(pub_keys["pub_key1"])
            session.pub_key_2 = int(pub_keys["pub_key2"])
            session.partial_key_client = int(pub_keys["partial_key_client"])
            encrypt = DHEncrypt(session["pub_key1"], session["pub_key2"], settings.DH_SECRET_KEY)
        except:
            return "Required keys are missing."
        session.partial_key_server = encrypt.generate_partial_key()
        session = self.__db_service.create_session(session)
        return session.partial_key_server


server_service = ServerService(db_service)
