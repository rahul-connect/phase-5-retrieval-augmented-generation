
"""Database engine and session configuration."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from rag.config import get_settings


settings = get_settings()

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for dependency injection."""

    with SessionLocal() as db:
        yield db
