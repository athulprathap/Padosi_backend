import uuid
from api.auth import crud, schemas
from api.utils import constantUtil, cryptoUtil, emailUtil, jwtUtil
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/api/v1"
) # type: APIRouter


# register router for /api/v1/auth/register

@router.post("/auth/register")  
async def register(user: schemas.UserCreate):

    # check user exist
    result = await crud.find_existed_user(user.email)
    if result:
        raise HTTPException(status_code=400, detail="User already exist")
    
    # create new user
    # hash password here 
    user.password = cryptoUtil.get_password_hash(user.password)
    await crud.save_user(user)

    return {**user.dict(), "message": "User created successfully"}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    # check user exist
    result = await crud.find_existed_user(form_data.username)
    if not result:
        raise HTTPException(status_code=400, detail="User not found")
    
    # verify password
    user = schemas.UserCreate(**result)
    verified_password = cryptoUtil.verify_password(form_data.password, user.password)
    if not verified_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # create token 
    access_token_expires = jwtUtil.timedelta(minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwtUtil.create_accces_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    results = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    results.update({
        "user_info": {
            "email": user.email,
            "fullname": user.fullname
        }
    })

    return results

@router.post("/auth/forgot-password")
async def forgot_password(request: schemas.ForgotPassword):
    # check user exist
    result = await crud.find_existed_user(request.email)
    if not result:
        raise HTTPException(status_code=400, detail="User not found")

    #create reset code and save in database
    reset_code = str(uuid.uuid4())
    await crud.create_reset_code(request.email, reset_code)

    # send email with reset code
    subject = "Reset Password"
    recipient = [request.email]
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">
        <h1>Hello, {0:}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
        <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={1:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """.format(request.email, reset_code)
    await emailUtil.send_email(subject, recipient, message)

    return {
        "reset_code": reset_code,
        "code": 200,
        "message": "We have sent an email to {0:} with a link to reset your password".format(request.email)
    }

@router.patch("/auth/reset-password")
async def reset_password(reset_password_token: str, request: schemas.ResetPassword):
    # check valid reset code
    reset_token = await crud.check_reset_password_token(reset_password_token)
    if not reset_token:
        raise HTTPException(status_code=404, detail="Reset password token has expired, please request a new one")
    
    # check both new and confirm password match
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=404, detail="New password and confirm password do not match")
    
    # Reset new password
    forgot_password_object = schemas.ForgotPassword(**reset_token)
    new_hashed_password = cryptoUtil.get_password_hash(request.new_password)
    await crud.reset_password(new_hashed_password,forgot_password_object.email)

    # Disable reset code
    await crud.disable_reset_code(reset_password_token, forgot_password_object.email)

    return {
        "code": 200,
        "message": "Password has been reset"
    }

