from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL


if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }
else:
    connect_args = {}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    future=True
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_db():
    from . import models

    Base.metadata.create_all(
        bind=engine
    )