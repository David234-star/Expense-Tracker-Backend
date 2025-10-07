import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv  # this should be here


load_dotenv()  # Loads variables from .env file


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
