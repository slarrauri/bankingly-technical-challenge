import os
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.domain.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aml_copilot.db")

# Handle SQLite connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(engine_instance=None) -> None:
    """Initialize all database tables defined in Base."""
    target_engine = engine_instance or engine
    Base.metadata.create_all(bind=target_engine)


def drop_db(engine_instance=None) -> None:
    """Drop all database tables defined in Base."""
    target_engine = engine_instance or engine
    Base.metadata.drop_all(bind=target_engine)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for acquiring and safely closing a database session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session."""
    with get_db_session() as session:
        yield session
