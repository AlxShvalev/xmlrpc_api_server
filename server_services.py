from datetime import datetime, timedelta
from uuid import UUID

from DH_encrypt import DHEncrypt
from db.models import Session, User
from db.services import DBService, db_service
from settings import settings


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

    def __session_is_expired(self, session: Session) -> Session:
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
        if session is None:
            raise Exception("Session id is incorrect.")
        session = self.__session_is_expired(session)
        try:
            session.pub_key_1 = int(pub_keys["pub_key1"])
            session.pub_key_2 = int(pub_keys["pub_key2"])
            session.partial_key_client = int(pub_keys["partial_key_client"])
        except:
            raise Exception("Required public keys are missing.")
        encrypt = DHEncrypt(session.pub_key_1, session.pub_key_2, settings.DH_SECRET_KEY)
        session.partial_key_server = encrypt.generate_partial_key()
        session = self.__db_service.update_session(session)
        return session.partial_key_server


server_service = ServerService(db_service)
