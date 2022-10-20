from passlib.context import CryptContext
import string
from starlette.config import Config
from random import choice
from twilio.rest import Client
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from starlette.config import Config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def random(digits: int):
    chars = string.digits
    return ''.join(choice(chars) for _ in range(digits))

config = Config(".env")

time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

client = Client(config('account_sid'),config('auth_token'))

# send a otp to phone using twiilo 
def OTP_send(msg, phone):
    message = client.messages.create(
        body=msg,
        from_=config('my_twilio'),
        to=phone
    )
    return message.sid

#load .env file
config = Config(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT"),
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_TLS = config("MAIL_TLS"),
    MAIL_SSL = config("MAIL_SSL"),
    USE_CREDENTIALS = config("USE_CREDENTIALS"),
    VALIDATE_CERTS = config("VALIDATE_CERTS")
)

async def send_email(subject: str, recipients: list, message: str):
    message = MessageSchema (
        subject=subject,
        recipients=recipients,
        body=message,
        subtype = "html"
    )

    mail = FastMail(conf)
    await mail.send_message(message)

