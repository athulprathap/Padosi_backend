from ctypes import util
import uuid
from fastapi import APIRouter, HTTPException
from .. import schema
from .. import utils
from app.enums import otp
from .. import model

router = APIRouter(
    prefix='/api/v1'
)


@router.post("/otp/send")
async def send_otp(
    type: otp.OTPType,
    request: schema.CreateOTP
):
    # Check block OTP
    opt_blocks = await model.find_otp_block(request.recipient_id)
    if opt_blocks:
        raise HTTPException(status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

    # Generate and save to table OTPs
    otp_code = utils.random(6)
    session_id = str(uuid.uuid1())
    await model.save_otp(request, session_id, otp_code)

    # Send OTP to email
    if type == otp.OTPType.email:
        # Sending email
        subject = "OTP Code"
        recipient = [request.recipient_id]
        message = """
            <!DOCTYPE html>
            <html>
            <title>Reset Password</title>
            <body>
            <div style="width:100%;font-family: monospace;">
                <h1>{0:}</h1>
            </div>
            </body>
            </html>
            """.format(otp_code)

        await utils.send_email(subject, recipient, message)

    else:
        # send otp to phone number
        msg = "Your OTP code is: " + otp_code
        await utils.OTP_send(msg, request.recipient_id)

    return {
        "session_id": session_id,
        "otp_code": otp_code
    }


@router.post("/otp/verify")
async def verify_otp(request: schema.VerifyOTP):
    # Check block OTP
    opt_blocks = await model.find_otp_block(request.recipient_id)
    if opt_blocks:
        raise HTTPException(status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

    # Check OTP code 6 digit life time
    otp_result = await model.find_otp_life_time(request.recipient_id, request.session_id)
    if not otp_result:
        raise HTTPException(status_code=404, detail="OTP code has expired, please request a new one.")

    otp_result = schema.InfoOTP(**otp_result)

    # Check if OTP code is already used
    if otp_result.status == "9":
        raise HTTPException(status_code=404, detail="OTP code has used, please request a new one.")

    # Verify OTP code, if not verified,
    if otp_result.otp_code != request.otp_code:
        # Increment OTP failed count
        await model.save_otp_failed_count(otp_result)

        # If OTP failed count = 5
        # then block otp
        if otp_result.otp_failed_count + 1 == 5:
            await model.save_block_otp(otp_result)
            raise HTTPException(status_code=404, detail="Sorry, this phone number is blocked in 5 minutes")

        # Throw exceptions
        raise HTTPException(status_code=404, detail="The OTP code you've entered is incorrect.")

    # Disable otp code when succeed verified
    await model.disable_otp(otp_result)

    return {
        "status_code": 200,
        "detail": "OTP verified successfully"
    }