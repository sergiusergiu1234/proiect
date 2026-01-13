from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, Session
from typing import  Generator
from config import getConfig
from model.base import Base
from model.review import Review
from model.processed_review import ProcessedReview

engine = create_engine("sqlite+pysqlite://", echo=True)
config = getConfig()

engine = create_engine(
    config.sqldbUrl,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
Base.metadata.create_all(engine)

def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

