from ctypes import util
import uuid
from fastapi import APIRouter, HTTPException
from .. import schema
from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List
from app.api.utils import random_with_N_digits
from app.api.utils import conf
from .. import schema
from .dynamic_link import DynamicLinks
import requests

router = APIRouter(
    prefix='/api/v1'
)


# @router.post("/otp/send")
# async def send_otp(
#     type: otp.OTPType,
#     request: schema.CreateOTP
# ):
#     # Check block OTP
#     opt_blocks = await find_otp_block(request.recipient_id)
#     if opt_blocks:
#         raise HTTPException(
#             status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

#     # Generate and save to table OTPs
#     otp_code = utils.random(6)
#     session_id = str(uuid.uuid1())
#     await save_otp(request, session_id, otp_code)

#     # Send OTP to email
#     if type == otp.OTPType.email:
#         # Sending email
#         subject = "OTP Code"
#         recipient = [request.recipient_id]
#         message = """
#             <!DOCTYPE html>
#             <html>
#             <title>Reset Password</title>
#             <body>
#             <div style="width:100%;font-family: monospace;">
#                 <h1>{0:}</h1>
#             </div>
#             </body>
#             </html>
#             """.format(otp_code)

#         await utils.send_email(subject, recipient, message)

#     else:
#         # send otp to phone number
#         msg = "Your OTP code is: " + otp_code
#         await utils.OTP_send(msg, request.recipient_id)

#     return {
#         "session_id": session_id,
#         "otp_code": otp_code
#     }


# @router.post("/otp/verify")
# async def verify_otp(request: schema.VerifyOTP):
#     # Check block OTP
#     opt_blocks = find_otp_block(request.recipient_id)
#     if opt_blocks:
#         raise HTTPException(
#             status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

#     # Check OTP code 6 digit life time
#     otp_result = await find_otp_life_time(request.recipient_id, request.session_id)
#     if not otp_result:
#         raise HTTPException(
#             status_code=404, detail="OTP code has expired, please request a new one.")

#     otp_result = schema.InfoOTP(**otp_result)

#     # Check if OTP code is already used
#     if otp_result.status == "9":
#         raise HTTPException(
#             status_code=404, detail="OTP code has used, please request a new one.")

#     # Verify OTP code, if not verified,
#     if otp_result.otp_code != request.otp_code:
#         # Increment OTP failed count
#         await save_otp_failed_count(otp_result)

#         # If OTP failed count = 5
#         # then block otp
#         if otp_result.otp_failed_count + 1 == 5:
#             await save_block_otp(otp_result)
#             raise HTTPException(
#                 status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

#         # Throw exceptions
#         raise HTTPException(
#             status_code=404, detail="The OTP code you've entered is incorrect.")

#     # Disable otp code when succeed verified
#     await disable_otp(otp_result)

#     return {
#         "status_code": 200,
#         "detail": "OTP verified successfully"
#     }


async def send_mail(email: schema.EmailSchema,request: Request):
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
