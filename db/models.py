from uuid import uuid4

from sqlalchemy import INT, TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.schema import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(INT, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(70), nullable=False)
    session = relationship("Session", back_populates="user")


class Data(Base):
    __tablename__ = "data"

    id = Column(INT, primary_key=True)
    key = Column(String(200), nullable=False)
    data = Column(String(1024), nullable=False)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(INT, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="session")
    expired_date = Column(TIMESTAMP, nullable=False)
    pub_key_1 = Column(INT)
    pub_key_2 = Column(INT)
    partial_key_client = Column(INT)
    partial_key_server = Column(INT)
    challenge = Column(String(1024))


if __name__ == "__main__":
    from db import engine
    Base.metadata.create_all(engine)
