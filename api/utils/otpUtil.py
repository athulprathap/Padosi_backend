from os import environ
import string
from starlette.config import Config
from random import choice
from twilio.rest import Client
from datetime import datetime

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
    





