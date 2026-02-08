"""
Database connection and session management for Phase II Todo App
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Convert postgresql:// to postgresql+psycopg2:// for sync support
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://")


# Create sync engine
if DATABASE_URL.startswith("sqlite:///"):
    # SQLite doesn't support pool_size and max_overflow
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,  # Verify connections before using
    )
else:
    # PostgreSQL supports connection pooling
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,
        max_overflow=20,
    )

# Create session factory
session = sessionmaker(
    engine,
    expire_on_commit=False,
)


def get_session():
    """
    Get database session for dependency injection.
    Usage in FastAPI:
        @app.get("/todos")
        def get_todos(session: Session = Depends(get_session)):
            ...
    """
    with session() as sess:
        yield sess


def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(bind=engine)


def close_db():
    """Close database connection pool"""
    engine.dispose()
