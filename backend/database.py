"""
Database configuration and session management for StadiumGPT.

Uses SQLAlchemy ORM with SQLite for the MVP. The database URL is
configurable via the DATABASE_URL environment variable.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./stadium.db")


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields a SQLAlchemy Session and ensures it is closed after use,
    even if an exception occurs during the request.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
