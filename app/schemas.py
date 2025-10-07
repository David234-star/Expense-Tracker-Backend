from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

# --- Expense Schemas ---
# Base schema for expense data


class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: str
    date: date
    is_recurring: Optional[bool] = False

# Schema for creating a new expense


class ExpenseCreate(ExpenseBase):
    pass

# Schema for reading/returning expense data


class Expense(ExpenseBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from ORM models

# --- User Schemas ---


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    expenses: List[Expense] = []

    class Config:
        from_attributes = True

# --- Token Schemas for JWT ---


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ------Password Reset-----

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    new_password: str
