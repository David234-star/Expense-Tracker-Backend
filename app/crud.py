import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import models, schemas, auth

# --- User CRUD Operations ---


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Password Reset / OTP Functions (NEW) ---


def create_otp_for_user(db: Session, user: models.User):
    """Generates a 6-digit OTP, saves it to the user record, and returns it."""
    otp = "{:06d}".format(secrets.randbelow(1000000))
    user.reset_token = otp  # Store the OTP in the reset_token column
    user.reset_token_expires = datetime.utcnow(
    ) + timedelta(hours=1)  # OTP is valid for 1 hour
    db.commit()
    return otp


def verify_user_otp(db: Session, email: str, otp: str):
    """
    Finds a user by email and checks if the provided OTP is valid and not expired.
    Includes debugging print statements.
    """
    user = get_user_by_email(db, email=email)

    # --- Start of Debugging Block ---
    print("--- Verifying OTP ---")
    print(f"Input Email: '{email}'")
    print(f"Input OTP: '{otp}'")

    if not user:
        print("Result: User not found in database.")
        print("--------------------")
        return None

    # Make the comparison robust by stripping whitespace
    stored_otp = user.reset_token.strip() if user.reset_token else None
    input_otp = otp.strip()

    print(f"Stored OTP in DB: '{stored_otp}'")
    print(f"Stored Expiration Time (UTC): {user.reset_token_expires}")
    print(f"Current Time (UTC): {datetime.utcnow()}")
    # --- End of Debugging Block ---

    # Perform the checks
    otp_matches = stored_otp == input_otp
    is_expired = not (
        user.reset_token_expires and user.reset_token_expires > datetime.utcnow())

    print(f"Does OTP match? {otp_matches}")
    print(f"Is OTP expired? {is_expired}")

    if otp_matches and not is_expired:
        print("Result: Success! OTP is valid.")
        print("--------------------")
        return user
    else:
        print("Result: Failure. OTP does not match or has expired.")
        print("--------------------")
        return None


def reset_user_password(db: Session, user: models.User, new_password: str):
    """Resets the user's password and clears the OTP token."""
    user.hashed_password = auth.get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()


# --- Expense CRUD Operations (Unchanged) ---

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
