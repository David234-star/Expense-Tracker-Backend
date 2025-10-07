from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    reset_token = Column(String, unique=True, index=True, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    # Relationship to expenses
    expenses = relationship("Expense", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True)
    date = Column(Date, nullable=False)
    is_recurring = Column(Boolean, default=False)

    # Foreign Key to link to the User table
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to the User
    owner = relationship("User", back_populates="expenses")
