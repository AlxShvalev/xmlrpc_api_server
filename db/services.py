from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from db.db import get_db_session
from db.models import Data, Session, User


class DBService:
    """Class for database interaction."""

    def __init__(self, db_session: DbSession):
        self.__db_session = db_session

    def get_user(self, username: str) -> User:
        """Get user from DB by username."""
        stmt = select(User).where(User.username == username)
        user = self.__db_session.execute(stmt)
        return user.scalars().first()

    def create_user(self, user: User) -> User:
        """Create new user in database."""
        self.__db_session.add(user)
        self.__db_session.commit()
        self.__db_session.refresh(user)
        return user

    def get_data(self, key: str) -> Data:
        """Get data from DB by data key."""
        stmt = select(Data).where(Data.key == key)
        data = self.__db_session.execute(stmt)
        return data.scalars().first()

    def get_session(self, session_id: UUID) -> Session:
        """Get session from db by session id."""
        stmt = select(Session).where(Session.id == session_id)
        session = self.__db_session.execute(stmt)
        return session.scalars().first()

    def get_session_by_user_id(self, user_id: int) -> Session:
        """Get session from DB by user id."""
        stmt = select(Session).where(Session.user_id == user_id)
        session = self.__db_session.execute(stmt)
        return session.scalars().first()

    def create_session(self, session: Session) -> Session:
        """Create new session in database."""
        self.__db_session.add(session)
        self.__db_session.commit()
        self.__db_session.refresh(session)
        return session

    def update_session(self, session: Session) -> Session:
        """Update existing session in database."""
        session = self.__db_session.merge(session)
        self.__db_session.commit()
        self.__db_session.refresh(session)
        return session

    def delete_session(self, session: Session) -> None:
        """Delete session from DB."""
        self.__db_session.delete(session)
        self.__db_session.commit()


db_service = DBService(get_db_session())
