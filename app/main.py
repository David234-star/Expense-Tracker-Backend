# app/main.py
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import io
import csv

from . import crud, models, schemas, auth
from .database import engine, get_db

# Create all database tables on application startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS (Cross-Origin Resource Sharing) Middleware ---
# This allows our React frontend (running on a different port/domain) to talk to our backend.
origins = [
    "http://localhost:3000",
    # Add your Vercel frontend URL here once deployed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === API ENDPOINTS ===

# --- Authentication ---


@app.get("/")
def read_root():
    """
    A simple endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Expense Tracker API! Visit /docs for documentation."}


@app.post("/signup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Current User ---


@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# --- Expense CRUD ---


@app.post("/expenses/", response_model=schemas.Expense, status_code=status.HTTP_201_CREATED)
def create_new_expense(expense: schemas.ExpenseCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.create_expense(db=db, expense=expense, user_id=current_user.id)


@app.get("/expenses/", response_model=List[schemas.Expense])
def get_user_expenses(skip: int = 0, limit: int = 100, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_expenses_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@app.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_existing_expense(expense_id: int, expense_update: schemas.ExpenseCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_expense = crud.update_expense(
        db, expense_id=expense_id, expense_update=expense_update, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_expense(expense_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_expense = crud.delete_expense(
        db, expense_id=expense_id, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Expense deleted successfully"}

# --- Optional Upgrade: Export to CSV ---


@app.get("/export/csv")
def export_expenses_to_csv(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    expenses = crud.get_expenses_by_user(
        db, user_id=current_user.id, limit=1000)  # Get all expenses

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['ID', 'Title', 'Amount', 'Category', 'Date', 'Recurring'])

    # Write data
    for expense in expenses:
        writer.writerow([expense.id, expense.title, expense.amount,
                        expense.category, expense.date, expense.is_recurring])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=expenses_{current_user.username}.csv"}
    )
