import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# --- THIS IS THE CORRECTED FUNCTION ---


async def send_otp_email(email: EmailStr, otp: str):
    html = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>You requested a password reset. Use the One-Time Password (OTP) below to reset your password.</p>
        <p style="font-size: 24px; font-weight: bold; letter-spacing: 4px; margin: 20px 0;">{otp}</p>
        <p>This OTP is valid for 1 hour. If you did not request this, please ignore this email.</p>
    </body>
    </html>
    """
    message = MessageSchema(
        subject="Your Password Reset OTP",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
