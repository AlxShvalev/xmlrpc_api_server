from datetime import datetime, timedelta
from uuid import UUID

from DH_encrypt import DHEncrypt
from db.models import Session, User
from db.services import DBService, db_service
from settings import settings


class ServerService:

    def __init__(self, db_service: DBService) -> None:
        self.__db_service = db_service

    def get_user(self, username: str, password: str) -> User:
        user = self.__db_service.get_user(username)
        if user is None:
            raise Exception("User not found.")
        if user.password != password:
            raise Exception("Password incorrect.")
        return user

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

    def __session_is_expired(self, session: Session) -> bool:
        return True if session.expired_date < datetime.now() else False

    def get_partial_key(self, session_id: UUID, pub_keys: dict) -> int:
        session = self.__db_service.get_session(session_id)
        if self.__session_is_expired(session):
            self.__db_service.delete_session(session)
            return "Session is expired. Please sign in again."
        try:
            session.pub_key_1 = int(pub_keys["pub_key1"])
            session.pub_key_2 = int(pub_keys["pub_key2"])
            session.partial_key_client = int(pub_keys["partial_key_client"])
        except:
            raise Exception("Required keys are missing.")
        encrypt = DHEncrypt(session.pub_key_1, session.pub_key_2, settings.DH_SECRET_KEY)
        session.partial_key_server = encrypt.generate_partial_key()
        session = self.__db_service.update_session(session)
        return session.partial_key_server


server_service = ServerService(db_service)
