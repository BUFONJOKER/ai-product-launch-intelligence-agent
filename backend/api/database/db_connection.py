from sqlalchemy import create_engine
from config import DB_URL_API
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy models in this project.

    All ORM model classes should inherit from `Base` so that SQLAlchemy
    can discover mapped tables and metadata when creating sessions and
    performing migrations.
    """

    pass


engine = create_engine(DB_URL_API)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Provide a transactional database session for FastAPI endpoints.

    This generator yields a SQLAlchemy `Session` instance and ensures
    it is properly closed after use. Use it as a dependency in FastAPI
    route handlers (e.g., `Depends(get_db)`).

    Yields:
        Session: A SQLAlchemy session bound to the configured engine.
    """

    with SessionLocal() as db:
        yield db
