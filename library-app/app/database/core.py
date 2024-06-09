from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    encoding="utf-8",
    echo=settings.SQLALCHEMY_ECHO,
)
if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

sBase = declarative_base()

metadata = MetaData()
if not engine.dialect.has_table(engine, settings.POSTGRES_DATABASE):
    metadata.create_all(engine)


class Base(sBase):  # type: ignore
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
