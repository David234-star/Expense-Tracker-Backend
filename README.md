# Expense Tracker API (FastAPI)

This is the backend for the Expense Tracker web application. It is a robust and secure RESTful API built with Python and FastAPI that handles user authentication, expense management, and data processing.

## Core Features

- **Secure Authentication**: Uses JWT (JSON Web Tokens) for secure user signup, login, and session management. API endpoints are protected, ensuring users can only access their own data.
- **Full CRUD Functionality**: Provides complete Create, Read, Update, and Delete operations for expense records.
- **Data Validation**: Leverages Pydantic models to ensure all incoming and outgoing data is well-structured and valid.
- **CSV Export**: An endpoint to export all of a user's expense data into a downloadable CSV file.
- **Database Agnostic**: Built with SQLAlchemy ORM, allowing for easy switching between SQLite (for development) and PostgreSQL (for production).
- **Containerized**: Includes a `Dockerfile` for easy, consistent deployment on services like Render.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: [Passlib](https://passlib.readthedocs.io/en/stable/) for password hashing, [python-jose](https://github.com/mpdavis/python-jose) for JWT management.
- **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database Drivers**: `psycopg2-binary` for PostgreSQL, `sqlite` for development.

---

## Getting Started

Follow these instructions to get the backend server running on your local machine.

### Prerequisites

- Python 3.9+
- `pip` package manager

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/David234-star/Expense-Tracker-Backend.git
    cd Expense-Tracker-Backend/backend
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the `backend` directory. Copy the contents of `.env.example` (or the block below) into it and fill in your details. **The `SECRET_KEY` should be a long, random, and secret string.**

    ```dotenv
    # .env

    # For JWT Authentication. Generate a long random string for SECRET_KEY.
    # You can generate one using: openssl rand -hex 32
    SECRET_KEY="YOUR_SUPER_LONG_AND_RANDOM_SECRET_KEY"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=60

    # For local SQLite development (default)
    DATABASE_URL="sqlite:///./sql_app.db"

    # For production with PostgreSQL, you would comment out the line above and use this:
    # DATABASE_URL="postgresql://user:password@host:port/dbname"
    ```

### Running the Application

With your virtual environment activated, run the Uvicorn server:

```bash
uvicorn app.main:app --reload
```

The API will now be running at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

| Method   | Endpoint                 | Protection | Description                                            |
| :------- | :----------------------- | :--------- | :----------------------------------------------------- |
| `POST`   | `/signup`                | Public     | Creates a new user account.                            |
| `POST`   | `/token`                 | Public     | Logs in a user and returns a JWT access token.         |
| `GET`    | `/users/me`              | Protected  | Retrieves the profile of the currently logged-in user. |
| `POST`   | `/expenses/`             | Protected  | Adds a new expense record for the current user.        |
| `GET`    | `/expenses/`             | Protected  | Retrieves all expense records for the current user.    |
| `PUT`    | `/expenses/{expense_id}` | Protected  | Updates an existing expense record.                    |
| `DELETE` | `/expenses/{expense_id}` | Protected  | Deletes an existing expense record.                    |
| `GET`    | `/export/csv`            | Protected  | Exports all user expenses to a CSV file.               |

## Deployment

This application is ready to be deployed on **Render**.

1.  Push your code to a GitHub repository.
2.  On Render, create a new "Web Service" and connect it to your repository.
3.  Set the runtime to **Docker**.
4.  Add the environment variables from your `.env` file to the Render environment settings. If using Render's PostgreSQL, use the provided internal `DATABASE_URL`.
5.  Deploy!
