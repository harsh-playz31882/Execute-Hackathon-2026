from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# SQLite database URL for local development
DATABASE_URL = "sqlite:///./energy_marketplace.db"


# The engine manages the connection to the SQLite database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite + threaded servers
)

# Session factory used in routes / services via dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """
    FastAPI-style dependency that yields a database session.
    Import and use with `Depends(get_db)` inside route functions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all database tables.

    Call this once on application startup to ensure the SQLite file
    and schema are created before serving requests.
    """
    # Local import to avoid circular dependency at module import time
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

