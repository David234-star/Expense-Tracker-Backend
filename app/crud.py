# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- User CRUD Operations ---


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Expense CRUD Operations ---


def get_expenses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Expense).filter(models.Expense.owner_id == user_id).offset(skip).limit(limit).all()


def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(**expense.dict(), owner_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense_update: schemas.ExpenseCreate, user_id: int):
    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id, models.Expense.owner_id == user_id).first()
    if db_expense:
        for key, value in expense_update.dict().items():
            setattr(db_expense, key, value)
        db.commit()
        db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id, models.Expense.owner_id == user_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense
