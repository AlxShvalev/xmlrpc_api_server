from sqlalchemy import select

from db.db import get_session
from db.models import Data, User


def get_user(username) -> User:
    session = get_session()
    stmt = select(User.username, User.password).where(User.username == username)
    user = session.execute(stmt)
    return user.first()


def get_data(key) -> Data:
    session = get_session()
    stmt = select(Data.key, Data.data).where(Data.key == key)
    data = session.execute(stmt)
    return data.first()
