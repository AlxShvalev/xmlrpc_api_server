from sqlalchemy import INT, Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(INT, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(70), nullable=False)


class Data(Base):
    __tablename__ = "data"

    id = Column(INT, primary_key=True)
    key = Column(String(200), nullable=False)
    data = Column(String(1024), nullable=False)


if __name__ == "__main__":
    from db import engine
    Base.metadata.create_all(engine)
