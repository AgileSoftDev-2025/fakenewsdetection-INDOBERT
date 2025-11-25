"""
Database configuration and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # Fix for SQLAlchemy 1.4+ (postgres:// -> postgresql://)
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=300,  # Recycle connections after 5 minutes
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency for getting database session
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Database not configured. Set DATABASE_URL environment variable."
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
