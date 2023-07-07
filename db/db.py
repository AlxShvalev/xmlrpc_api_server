from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from settings import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(engine, class_=Session)


def get_session():
    with SessionLocal() as session:
        return session
