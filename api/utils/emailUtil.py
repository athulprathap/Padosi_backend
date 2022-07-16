from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from starlette.config import Config

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