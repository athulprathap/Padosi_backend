from passlib.context import CryptContext
import string
from fastapi import status, HTTPException, Depends, APIRouter
# from starlette.config import Config
from random import choice
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from datetime import date, datetime
from pyfcm import FCMNotification
from . import model
from app.api.config import settings
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Dict, List
from random import randint
from app.api import schema
from starlette.responses import JSONResponse
from starlette.config import Config
from app.api.schema import UserDevicePayload, MessagePayload
from app.api.crud import save, send
from app.api.routes.dynamic_link import DynamicLinks
import requests

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def random(digits: int):
    chars = string.digits
    return ''.join(choice(chars) for _ in range(digits))

async def send_mobile_otp(db, mobile_no, otp):
    client = Client(config.settings.twilio_account_sid, config.settings.twilio_auth_token)
    otp = str(otp)
    message = client.messages \
                    .create(
                        body="your otp for padosii is "+ otp,
                        from_=config.settings.twilio_number,
                        to=mobile_no
                    )
    if message:
        return True
    return False
# async def register_dev

# config = Config(".env")

# time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# client = Client(config('account_sid'),config('auth_token'))

# # send a otp to phone using twiilo 
# def OTP_send(msg, phone):
#     message = client.messages.create(
#         body=msg,
#         from_=config('my_twilio'),
#         to=phone
#     )
#     return message.sid

#load .env file
config = Config(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT"),
    MAIL_SERVER = config("MAIL_SERVER"),
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

def calculateAge(birthDate):
	today = date.today()
	age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
	return age

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

async def send_mobile_otp(mobile_no):
    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        verify = client.verify.services(settings.twilio_verify_service_sid)
        verify.verifications.create(to=mobile_no,channel='sms')
        return ("OTP sent successfully")
    except TwilioRestException as e:
        print(e)
        return ("Unable to send OTP")

async def verify_otp(mobile_no,otp):
    try:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        verify = client.verify.services(settings.twilio_verify_service_sid)
        result = verify.verification_checks.create(to=mobile_no, code=otp)
        # return ("OTP sent successfully")
        return (result.status)
    except TwilioRestException as e:
        print(e)
        return ("Unable to verify OTP")

    # client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    # verify = client.verify.services(settings.twilio_verify_service_sid)
    # return verify.verifications.create(to=mobile_no,channel='sms')
    # otp = str(otp)
    # message = client.messages \
    #                 .create(
    #                     body="your otp for padosii is "+ otp,
    #                     from_=settings.twilio_number,
    #                     to=mobile_no
    #                 )
    # if message:
    #     return True
    # return Fa

# async def push_notification(device_token, data):
#     push_service = FCMNotification(
#         api_key=SERVER_KEY)

#     try:
#         push_service.notify_single_device(registration_id=device_token, data_message=data)
#         print("message sent")
#     except:
#         return False
#     return True
async def register_device(user_device: UserDevicePayload):
    return await save(user_device)


async def send_message(message: MessagePayload):
    return await send(message)

async def send_mail(email: schema.EmailSchema,request: requests):
    otp = random_with_N_digits(6)
    api_key = "AIzaSyBB5bZP3g8e84jeCppKrgxwxhZ85j8JeBE"
    domain = "https://padosii.page.link"
    timeout = 10
    # params = {
    #     "androidInfo": {
    #         "androidPackageName": "com.app.padosii",
    #         "androidFallbackLink": f"{request.url}/reset-password?code={otp}",
    #         "androidMinPackageVersionCode": "1.0.0"
    #     },
    #     "iosInfo": {
    #         "iosBundleId": "com.app.padosii",
    #         "iosFallbackLink": f"{request.url}/reset-password?code={otp}"
    #     },
    # }
    params = {
    "androidInfo": {
      "androidPackageName":"com.app.padosii",
      "androidFallbackLink": f"{request.url}/reset-password?code={otp}"
    },
    "iosInfo": {
      "iosBundleId": "com.app.padosii",
      "iosFallbackLink": f"{request.url}/reset-password?code={otp}"
    }
}
    print(f"{request.url}/reset-password?code={otp}")
    dl = DynamicLinks(api_key, domain, timeout)
    short_link = dl.generate_dynamic_link(f"{request.url}/reset-password?code={otp}",True,params)
    body_message = """
            <!DOCTYPE html>
            <html>
            <title>Reset Password</title>
            <body>
            <p>We heard that you lost your password. Sorry about that!</p>

<p>But don’t worry! You can use the following link to reset your password:</p>
<a href="{0:}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 10px;">Reset Password</a>

<p>Thanks.</p>
            </body>
            </html>

            
            """.format(short_link)
    message = MessageSchema(
        subject="Padosii OTP",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=body_message,
        subtype="html"

        )

    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
