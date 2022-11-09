from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..model import User
from ..schema import Token
from .. import  utils, schema
from ..database import get_db
from .. utils import random_with_N_digits
from app.api.routes.otp import send_mail
from  ..oauth2 import get_current_user,get_current_active_user,access_token

router = APIRouter(tags = ['Login'])

@router.post('/login', response_model=Token)
async def login_user(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_info.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    if not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password")

    token = access_token(data={"users_id": user.id})

    return {"access_token": token,"token_type": "bearer"}

@router.post('/email/login')
def email_login(userdata: schema.EmailSchema, db: Session=Depends(get_db)):
    user_query = db.query(User).filter(
        User.username == userdata.email)
    user = user_query.first()

    if not user:
        otp = str(random_with_N_digits(6))
        password = utils.hash(otp)
        new_user = User(**userdata.dict(),username=userdata.email, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token = access_token(data = {"user_id": new_user.id})
        return {"already_exist":False, "access_token" : access_token,"token_type" : "bearer"}
    user_profile = db.query(User).filter(User.id==user.id).first()
    if not user_profile:
        access_token = access_token(data = {"user_id": user.id})
        return {"already_exist":False, "access_token" : access_token}

    access_token = access_token(data = {"user_id": user.id})
    return {"already_exist":True, "access_token" : access_token}

@router.post("/send-reset")
async def reset_password(userdata: schema.UserCreate,db: Session=Depends(get_db)):
    user_query = db.query(User).filter(
        User.email == userdata.email)
    user = user_query.first()
    if user:
        status = await send_mail(userdata.email)

        if status:
            return {"message":"success"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="reset link send failed")
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found")


@router.post("/set-password")
def set_password(userdata:schema.SetPassword, db: Session=Depends(get_db)):
    user_query = db.query(User).filter(
        User.username == userdata.email,
        User.passcode == userdata.passcode,
        User.is_deleted == False)
    user = user_query.first()
    if user:
        password = utils.hash(userdata.password)
        user_query.update({"password":password})
        db.commit()
        return {"message":"success"}
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found")