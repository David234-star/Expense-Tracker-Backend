# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file

# Get the Database URL from environment variables
# It falls back to a local SQLite database if not found.
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
# The 'check_same_thread' argument is only needed for SQLite.
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Each instance of the SessionLocal class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from.
Base = declarative_base()

# Dependency to get a DB session in our API endpoints


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
