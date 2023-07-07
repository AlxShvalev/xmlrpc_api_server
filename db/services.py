from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.db import get_db_session
from db.models import Data, Session, User


class DBService:
    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def get_user(self, username) -> User:
        stmt = select(User.id, User.username, User.password).where(User.username == username)
        user = self.__db_session.execute(stmt)
        return user.first()

    def get_data(self, key) -> Data:
        stmt = select(Data.key, Data.data).where(Data.key == key)
        data = self.db_session.execute(stmt)
        return data.first()

    def get_session(self, session_id: UUID) -> Session:
        stmt = select(
            Session.id,
            Session.user_id,
            Session.expired_date,
            Session.pub_key_1,
            Session.pub_key_2,
            Session.partial_key_client,
            Session.partial_key_server,
            Session.challenge
        ).where(Session.id == session_id)
        session = self.__db_session.execute(stmt)
        return session.first()

    def create_session(self, session: Session) -> Session:
        self.__db_session.add(session)
        self.__db_session.commit()
        self.__db_session.refresh(session)
        return session


db_service = DBService(get_db_session())
