from passlib.context import CryptContext
import string
from starlette.config import Config
from random import choice
from twilio.rest import Client
from . import model
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Dict, List
from random import randint
from starlette.responses import JSONResponse
from starlette.config import Config
from app.api.schema import UserDevicePayload, MessagePayload
# from .crud import save,send


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
    MAIL_STARTTLS = config("MAIL_STARTTLS"),
    MAIL_SSL_TLS = config("MAIL_SSL_TLS"),
    MAIL_TLS = config("MAIL_TLS"),
    MAIL_SSL = config("MAIL_SSL"),
    USE_CREDENTIALS = config("USE_CREDENTIALS"),
    VALIDATE_CERTS = config("VALIDATE_CERTS")
)

async def send_email(otp,subject: str, recipients: list, message: str):
    body_message = "user otp for schwooze is :" + str(otp)
    message = MessageSchema (
        subject=subject,
        recipients=recipients,
        body=message,
        subtype = "html"
    )

    mail = FastMail(conf)
    await mail.send_message(message)


async def send_otp_mail(email, otp):
    body_message = "user otp for padosii is :" + str(otp)
    message = MessageSchema(
        subject="padosii OTP",
        recipients=[email],
        body=body_message,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


def operation_after_block(db, blocker_user, blocked_user):
    blocker_query = db.query(model.UserRecommadation).filter(
        model.UserRecommadation.user_id == blocked_user,
        model.UserRecommadation.self_user_id == blocker_user)

    blocked_query = db.query(model.UserRecommadation).filter(
        model.UserRecommadation.user_id == blocker_user,
        model.UserRecommadation.self_user_id == blocked_user)

    if blocker_query.first():
        blocker_query.delete()
    if blocked_query.first():
        blocked_query.delete()
    return True


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

async def password_reset(subject:str, email_to: str, body:Dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html"
    ),
    fm =FastMail(conf)
    await fm.send_message(message, template_name="password_reset.html")

# async def register_device(user_device: UserDevicePayload):
#     return await save(user_device)


# async def send_message(message: MessagePayload):
#     return await send(message)
